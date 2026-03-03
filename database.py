import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def salvar_item_estudo(tabela, dados):
    """Insere dados diretamente no Big Data"""
    try:
        return get_supabase().table(tabela).insert(dados).execute()
    except Exception as e:
        return None

def listar_biblioteca_global(tabela="flashcards", area="Clínica Médica", limit=50):
    try:
        res = get_supabase().table(tabela).select("*").eq("is_global", True).eq("grande_area", area).limit(limit).execute()
        return res.data if res.data else []
    except:
        return []

def validar_login(email, senha):
    try:
        res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
        return res.data[0] if res.data else None
    except: return None
