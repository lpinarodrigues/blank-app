import streamlit as st
from supabase import create_client
import pandas as pd

# Conexão Central
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- 1. AUTENTICAÇÃO (Sincronizado com o Login) ---
def validar_login(email, senha):
    try:
        res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
        return res.data[0] if res.data else None
    except: return None

def cadastrar_membro(nome, email, senha):
    try:
        # Verifica duplicidade
        check = get_supabase().table("membros_core").select("email").eq("email", email).execute()
        if check.data: return False
        
        get_supabase().table("membros_core").insert({
            "nome": nome, "email": email, "senha": senha, "score": 0
        }).execute()
        return True
    except Exception as e:
        st.error(f"Erro no cadastro: {e}")
        return False

# --- 2. LISTAGEM E ESTUDOS (Sincronizado com Master Study) ---
def listar_flashcards(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).execute()
        return res.data if res.data else []
    except: return []

def listar_biblioteca_global(area="Clínica Médica", subtema="Cardiologia", limit=100):
    try:
        query = get_supabase().table("flashcards").select("*").eq("is_global", True)
        if area != "Todas": query = query.eq("grande_area", area)
        res = query.limit(limit).execute()
        return res.data if res.data else []
    except: return []

# --- 3. MOTOR DE BIG DATA E REPETIÇÃO ---
def salvar_item_estudo(dados):
    """Injeção massiva de questões e cards"""
    try:
        return get_supabase().table("flashcards").insert(dados).execute()
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
        return None

def atualizar_progresso_sm2(card_id, qualidade):
    dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
    proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
    get_supabase().table("flashcards").update({
        "proxima_revisao": proxima, 
        "facilidade": 2.5 + (qualidade * 0.1)
    }).eq("id", card_id).execute()

# --- 4. PERFORMANCE ---
def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        return res.data[0]['score'] if res.data else 0
    except: return 0
