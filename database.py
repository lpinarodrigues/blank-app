import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- AUTH ---
def validar_login(email, senha):
    try:
        res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
        return res.data[0] if res.data else None
    except: return None

# --- LISTAGEM (O que estava dando erro) ---
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

# --- INSERÇÃO MASSIVA ---
def salvar_item_estudo(dados):
    try:
        return get_supabase().table("flashcards").insert(dados).execute()
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return None

def atualizar_progresso_sm2(card_id, qualidade):
    dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
    proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
    get_supabase().table("flashcards").update({"proxima_revisao": proxima, "facilidade": 2.5 + (qualidade * 0.1)}).eq("id", card_id).execute()
