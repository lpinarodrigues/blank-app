import streamlit as st
from supabase import create_client, Client

def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def get_core_score(email):
    supabase = get_supabase()
    response = supabase.table("usuarios").select("score").eq("email", email).execute()
    if response.data:
        return response.data[0]['score']
    return 0

def update_score(email, points):
    supabase = get_supabase()
    current_score = get_core_score(email)
    new_score = current_score + points
    supabase.table("usuarios").update({"score": new_score}).eq("email", email).execute()
    return new_score
