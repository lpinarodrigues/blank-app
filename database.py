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
        check = get_supabase().table("membros_core").select("email").eq("email", email).execute()
        if check.data: return False
        get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
        return True
    except: return False

# --- 2. PERFORMANCE E ANALYTICS ---
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

def obter_estatisticas_estudo(email):
    """Retorna dados para o Radar Chart e Gráficos de Retenção"""
    try:
        res = get_supabase().table("flashcards").select("grande_area, subtema, facilidade, revisões_totais").eq("criado_por_email", email).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except: return pd.DataFrame()

def sugerir_foco_ia(df_stats):
    if df_stats.empty: return "Inicie seus estudos para análise."
    try:
        # Pega a categoria com menor facilidade média
        foco = df_stats.groupby('grande_area')['facilidade'].mean().idxmin()
        return foco
    except: return "Geral"

# --- 3. ESTUDOS E HIERARQUIA ---
def salvar_flashcard_estruturado(p, r, area, subtema, tema, email, exp="", nivel=2):
    get_supabase().table("flashcards").insert({
        "pergunta": p, "resposta": r, "grande_area": area,
        "subtema": subtema, "categoria": tema, "criado_por_email": email, 
        "explicacao": exp, "complexidade": nivel
    }).execute()

def salvar_flashcard(p, r, cat, email):
    salvar_flashcard_estruturado(p, r, "Clínica Médica", "Geral", cat, email)

def listar_flashcards(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).order("id").execute()
        return res.data if res.data else []
    except: return []

def atualizar_revisao_card(card_id, qualidade):
    # Lógica de intervalo simplificada para o banco
    get_supabase().table("flashcards").update({
        "facilidade": 2.5 + (qualidade * 0.1),
        "revisões_totais": 1 # Em prod isso incrementaria
    }).eq("id", card_id).execute()

# --- 4. GESTÃO DE QUESTÕES ---
def salvar_questao_banco(dados):
    try:
        get_supabase().table("questionarios").insert(dados).execute()
    except: pass
