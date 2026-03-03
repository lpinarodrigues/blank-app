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

def cadastrar_membro(nome, email, senha):
    try:
        get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
        return True
    except: return False

# --- 2. MOTOR DE REPETIÇÃO ESPAÇADA (SM-2) E ESTUDOS ---
def atualizar_progresso_sm2(card_id, qualidade):
    """Calcula a próxima revisão baseada na qualidade da resposta (1-5)"""
    try:
        # Intervalo simples: qualidade 5 = 15 dias, qualidade 1 = hoje
        dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
        proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
        
        get_supabase().table("flashcards").update({
            "facilidade": 2.5 + (qualidade * 0.1),
            "proxima_revisao": proxima,
            "revisões_totais": 1
        }).eq("id", card_id).execute()
    except Exception as e:
        st.error(f"Erro ao agendar revisão: {e}")

def filtrar_banco_elite(area=None, subtema=None):
    """Busca cards filtrados por Grande Área ou Subtema"""
    try:
        query = get_supabase().table("flashcards").select("*")
        if area and area != "Todas": query = query.eq("grande_area", area)
        if subtema and subtema != "Todos": query = query.eq("subtema", subtema)
        res = query.execute()
        return res.data if res.data else []
    except: return []

# --- 3. ANALYTICS E PERFORMANCE ---
def obter_estatisticas_estudo(email):
    try:
        res = get_supabase().table("flashcards").select("grande_area, subtema, facilidade").eq("criado_por_email", email).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except: return pd.DataFrame()

def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        return res.data[0]['score'] if res.data else 0
    except: return 0

def obter_ranking_elite():
    try:
        res = get_supabase().table("membros_core").select("nome, score").order("score", desc=True).limit(5).execute()
        return res.data if res.data else []
    except: return []

# --- 4. INSERÇÃO DE DADOS ---
def salvar_item_estudo(dados):
    return get_supabase().table("flashcards").insert(dados).execute()

def salvar_flashcard_estruturado(p, r, area, subtema, tema, email, exp="", nivel=2):
    salvar_item_estudo({
        "pergunta": p, "resposta": r, "grande_area": area,
        "subtema": subtema, "categoria": tema, "criado_por_email": email, 
        "explicacao": exp, "complexidade": nivel
    })
