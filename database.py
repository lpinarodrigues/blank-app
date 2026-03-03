import streamlit as st
from supabase import create_client
import pandas as pd

# Conexão Central
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- 1. AUTENTICAÇÃO (Sincronizado com Login/Cadastro) ---
def validar_login(email, senha):
    try:
        res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
        return res.data[0] if res.data else None
    except: return None

def cadastrar_membro(nome, email, senha):
    try:
        check = get_supabase().table("membros_core").select("email").eq("email", email).execute()
        if check.data: return False
        get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
        return True
    except: return False

# --- 2. ESTUDOS E BIBLIOTECAS (O que estava faltando) ---
def listar_flashcards(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("is_global", False).execute()
        return res.data if res.data else []
    except: return []

def listar_biblioteca_global(area="Clínica Médica", subtema="Cardiologia", limit=100):
    try:
        query = get_supabase().table("flashcards").select("*").eq("is_global", True)
        if area != "Todas": query = query.eq("grande_area", area)
        res = query.limit(limit).execute()
        return res.data if res.data else []
    except: return []

def adotar_item_global(item_id, novo_email):
    """Clona um item da Global para a Pessoal do usuário"""
    try:
        supabase = get_supabase()
        item = supabase.table("flashcards").select("*").eq("id", item_id).single().execute().data
        if item:
            new_item = item.copy()
            del new_item['id']
            if 'created_at' in new_item: del new_item['created_at']
            new_item['criado_por_email'] = novo_email
            new_item['is_global'] = False
            supabase.table("flashcards").insert(new_item).execute()
            return True
    except: return False

# --- 3. MOTOR SM-2 E ANALYTICS ---
def atualizar_progresso_sm2(card_id, qualidade):
    try:
        dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
        proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
        get_supabase().table("flashcards").update({"proxima_revisao": proxima, "facilidade": 2.5 + (qualidade * 0.1)}).eq("id", card_id).execute()
    except: pass

def obter_estatisticas_estudo(email):
    try:
        res = get_supabase().table("flashcards").select("grande_area, subtema, facilidade").eq("criado_por_email", email).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except: return pd.DataFrame()

# --- 4. BIG DATA INJECTION ---
def salvar_item_estudo(dados):
    try:
        return get_supabase().table("flashcards").insert(dados).execute()
    except: return None

def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        return res.data[0]['score'] if res.data else 0
    except: return 0
