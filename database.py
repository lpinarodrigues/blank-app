import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- CORE DATA ENGINE ---
def salvar_item_estudo(dados):
    """Salva questões ou flashcards com hierarquia total"""
    get_supabase().table("flashcards").insert(dados).execute()

def filtrar_banco_elite(area=None, subtema=None):
    query = get_supabase().table("flashcards").select("*")
    if area and area != "Todas": query = query.eq("grande_area", area)
    if subtema and subtema != "Todos": query = query.eq("subtema", subtema)
    res = query.execute()
    return res.data if res.data else []

def atualizar_progresso_sm2(card_id, qualidade):
    # Algoritmo de Repetição Espaçada (SM-2 Simplificado)
    proxima = (pd.Timestamp.now() + pd.Timedelta(days=qualidade*2)).isoformat()
    get_supabase().table("flashcards").update({
        "facilidade": 2.5 + (qualidade * 0.1),
        "proxima_revisao": proxima,
        "revisões_totais": 1
    }).eq("id", card_id).execute()

def obter_estatisticas_estudo(email):
    res = get_supabase().table("flashcards").select("grande_area, subtema, facilidade").eq("criado_por_email", email).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

def cadastrar_membro(nome, email, senha):
    try:
        get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
        return True
    except: return False

def validar_login(email, senha):
    res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
    return res.data[0] if res.data else None

def get_core_score(email):
    res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
    return res.data[0]['score'] if res.data else 0

def obter_ranking_elite():
    res = get_supabase().table("membros_core").select("nome, email, score").order("score", desc=True).limit(5).execute()
    return res.data if res.data else []
