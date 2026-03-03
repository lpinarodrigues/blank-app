import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def salvar_item_estudo(dados):
    return get_supabase().table("flashcards").insert(dados).execute()

def filtrar_banco_elite(area=None, subtema=None):
    try:
        query = get_supabase().table("flashcards").select("*")
        if area and area != "Todas": query = query.eq("grande_area", area)
        if subtema and subtema != "Todos": query = query.eq("subtema", subtema)
        res = query.execute()
        return res.data if res.data else []
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return []

def obter_ranking_elite():
    try:
        res = get_supabase().table("membros_core").select("nome, score").order("score", desc=True).limit(5).execute()
        return res.data
    except: return []

def validar_login(email, senha):
    res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
    return res.data[0] if res.data else None

def get_core_score(email):
    res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
    return res.data[0]['score'] if res.data else 0
