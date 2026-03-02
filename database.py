import streamlit as st
from supabase import create_client

def get_supabase():
    # Tenta ler do secrets do Streamlit Cloud ou Local
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def get_core_score(email):
    try:
        supabase = get_supabase()
        response = supabase.table("usuarios").select("score").eq("email", email).execute()
        if response.data:
            return response.data[0]['score']
        return 0
    except Exception as e:
        return 0 # Retorno seguro caso a tabela ainda não exista

def update_score(email, points):
    supabase = get_supabase()
    current = get_core_score(email)
    new_score = current + points
    supabase.table("usuarios").upsert({"email": email, "score": new_score}).execute()
    return new_score
