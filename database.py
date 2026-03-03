import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- NAVEGAÇÃO E LISTAGEM (O que estava faltando) ---
def listar_flashcards(email):
    """Lista cards pessoais do usuário"""
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("is_global", False).execute()
        return res.data if res.data else []
    except: return []

def listar_biblioteca_global(tipo="flashcard", limit=50):
    """Lista itens do Big Data para adoção"""
    try:
        res = get_supabase().table("flashcards").select("*").eq("is_global", True).limit(limit).execute()
        return res.data if res.data else []
    except: return []

# --- MOTOR DE REPETIÇÃO E PERFORMANCE ---
def atualizar_progresso_sm2(card_id, qualidade):
    dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
    proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
    get_supabase().table("flashcards").update({
        "facilidade": 2.5 + (qualidade * 0.1),
        "proxima_revisao": proxima,
        "revisões_totais": 1
    }).eq("id", card_id).execute()

# --- PAINEL DE ADMIN (Sua visão exclusiva) ---
def obter_metricas_admin():
    """Retorna o que os 4000 itens estão gerando de dados"""
    supabase = get_supabase()
    total_cards = supabase.table("flashcards").select("id", count="exact").execute().count
    total_membros = supabase.table("membros_core").select("id", count="exact").execute().count
    # Top temas com mais erros (Simulado por facilidade baixa)
    erros = supabase.table("flashcards").select("grande_area, facilidade").lt("facilidade", 2.0).execute().data
    return total_cards, total_membros, pd.DataFrame(erros) if erros else pd.DataFrame()

# --- AUTENTICAÇÃO E RANKING ---
def validar_login(email, senha):
    res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
    return res.data[0] if res.data else None

def cadastrar_membro(nome, email, senha):
    get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
    return True

def get_core_score(email):
    res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
    return res.data[0]['score'] if res.data else 0
