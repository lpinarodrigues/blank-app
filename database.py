import streamlit as st
from supabase import create_client
import pandas as pd

# Conexão Central
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- 1. AUTENTICAÇÃO ---
def validar_login(email, senha):
    try:
        res = get_supabase().table("membros_core").select("*").eq("email", email).eq("senha", senha).execute()
        return res.data[0] if res.data else None
    except: return None

def criar_usuario(nome, email, senha):
    try:
        get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
        return True
    except: return False

# --- 2. PERFORMANCE E SCORE ---
def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        return res.data[0]['score'] if res.data else 0
    except: return 0

def update_score(email, pontos):
    try:
        score_atual = get_core_score(email)
        get_supabase().table("membros_core").update({"score": score_atual + pontos}).eq("email", email).execute()
    except: pass

def obter_ranking_elite():
    try:
        res = get_supabase().table("membros_core").select("nome, email, score").order("score", desc=True).limit(10).execute()
        return res.data if res.data else []
    except: return []

# --- 3. ESTUDOS E HIERARQUIA (PADRÃO OURO) ---
def salvar_flashcard_estruturado(p, r, area, subtema, tema, email, exp="", nivel=2):
    get_supabase().table("flashcards").insert({
        "pergunta": p, "resposta": r, "grande_area": area,
        "subtema": subtema, "categoria": tema, "criado_por_email": email, 
        "explicacao": exp, "complexidade": nivel
    }).execute()

def listar_flashcards(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).execute()
        return res.data if res.data else []
    except: return []

def atualizar_revisao_card(card_id, qualidade):
    # Lógica de repetição espaçada simplificada no DB
    get_supabase().table("flashcards").update({"revisões_totais": 1}).eq("id", card_id).execute()

# Função genérica de flashcards (compatibilidade)
def salvar_flashcard(p, r, cat, email):
    salvar_flashcard_estruturado(p, r, "Geral", "Geral", cat, email)
