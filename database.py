import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- FUNÇÕES DE LISTAGEM ---
def listar_flashcards(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("is_global", False).execute()
        return res.data if res.data else []
    except: return []

def listar_biblioteca_global(tipo="flashcard", limit=50):
    try:
        res = get_supabase().table("flashcards").select("*").eq("is_global", True).limit(limit).execute()
        return res.data if res.data else []
    except: return []

# --- FUNÇÃO DE ADOÇÃO (O que estava faltando) ---
def adotar_item_global(item_id, novo_email):
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
    except Exception as e:
        st.error(f"Erro ao adotar item: {e}")
    return False

# --- PERFORMANCE E LOGIN ---
def atualizar_progresso_sm2(card_id, qualidade):
    dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
    proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
    get_supabase().table("flashcards").update({"proxima_revisao": proxima, "facilidade": 2.5 + (qualidade * 0.1)}).eq("id", card_id).execute()

def validar_login(email, senha):
    res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
    return res.data[0] if res.data else None

def cadastrar_membro(nome, email, senha):
    get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
    return True
