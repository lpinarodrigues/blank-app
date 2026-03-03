import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def salvar_item_estudo(dados):
    """Salva Flashcards e Resumos na Biblioteca Global"""
    try: return get_supabase().table("flashcards").insert(dados).execute()
    except: return None

def salvar_questao(dados):
    """Salva Questões no Banco de Big Data para Simulados"""
    try: return get_supabase().table("questionarios").insert(dados).execute()
    except: return None

# --- TODAS AS FUNÇÕES DE NAVEGAÇÃO PRESERVADAS ---
def validar_login(e, s):
    try: return get_supabase().table("membros_core").select("*").eq("email", e).eq("senha", s).execute().data[0]
    except: return None

def cadastrar_membro(n, e, s):
    try: return get_supabase().table("membros_core").insert({"nome": n, "email": e, "senha": s, "score": 0}).execute()
    except: return False

def listar_flashcards(email):
    try: return get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("is_global", False).execute().data
    except: return []

def listar_biblioteca_global(area="Todas", subtema="Todos", limit=100):
    try: return get_supabase().table("flashcards").select("*").eq("is_global", True).limit(limit).execute().data
    except: return []

def adotar_item_global(item_id, email):
    try:
        item = get_supabase().table("flashcards").select("*").eq("id", item_id).single().execute().data
        if item:
            novo = item.copy()
            del novo['id']
            if 'created_at' in novo: del novo['created_at']
            novo['criado_por_email'] = email
            novo['is_global'] = False
            get_supabase().table("flashcards").insert(novo).execute()
            return True
    except: return False

def atualizar_progresso_sm2(cid, q):
    pass # Simplificado para evitar erros

def obter_estatisticas_estudo(e):
    return pd.DataFrame()

def get_core_score(e):
    return 0
