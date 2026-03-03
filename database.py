import streamlit as st
from supabase import create_client

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- GESTÃO DE MEMBROS ---
def validar_login(email, senha):
    supabase = get_supabase()
    res = supabase.table("membros_core").select("*").eq("email", email).eq("senha", senha).eq("aprovado", True).execute()
    return res.data[0] if res.data else None

def cadastrar_membro(nome, email, tel, vinculo, senha):
    supabase = get_supabase()
    return supabase.table("membros_core").insert({
        "nome": nome, "email": email, "tel": tel, "vinculo": vinculo, "senha": senha
    }).execute()

# --- GESTÃO DE CONTEÚDO ---
def salvar_flashcard(pergunta, resposta, categoria, email):
    get_supabase().table("flashcards").insert({
        "pergunta": pergunta, "resposta": resposta, "categoria": categoria, "criado_por_email": email
    }).execute()

def listar_questoes(categoria=None):
    query = get_supabase().table("questionarios").select("*")
    if categoria:
        query = query.eq("categoria", categoria)
    return query.execute().data

# --- PERFORMANCE ---
def registrar_performance(email, respondidas, acertos):
    percent = (acertos / respondidas * 100) if respondidas > 0 else 0
    get_supabase().table("resultados_performance").insert({
        "user_email": email, "questoes_respondidas": respondidas, "acertos": acertos, "aproveitamento_percent": percent
    }).execute()
