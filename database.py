import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- 1. AUTENTICAÇÃO ---
def validar_login(e, s):
    try: return get_supabase().table("membros_core").select("*").eq("email", e).eq("senha", s).execute().data[0]
    except: return None

def cadastrar_membro(nome, email, senha):
    try:
        check = get_supabase().table("membros_core").select("email").eq("email", email).execute()
        if check.data: return False
        get_supabase().table("membros_core").insert({"nome": nome, "email": email, "senha": senha, "score": 0}).execute()
        return True
    except: return False

def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        if res.data and isinstance(res.data, list) and isinstance(res.data[0], dict): return res.data[0].get('score', 0)
        return 0
    except: return 0

# --- 2. MOTOR DE REPETIÇÃO ESPAÇADA (SM-2) - O erro estava aqui ---
def atualizar_progresso_sm2(card_id, qualidade):
    """Atualiza a próxima revisão baseado na qualidade da resposta (1 a 5)"""
    try:
        dias = {1: 0, 3: 3, 4: 7, 5: 15}.get(qualidade, 1)
        proxima = (pd.Timestamp.now() + pd.Timedelta(days=dias)).isoformat()
        get_supabase().table("flashcards").update({"proxima_revisao": proxima, "facilidade": 2.5 + (qualidade * 0.1)}).eq("id", card_id).execute()
    except: pass

# --- 3. ESTUDO ATIVO E BIBLIOTECA ---
def salvar_item_estudo(dados):
    try: return get_supabase().table("flashcards").insert(dados).execute()
    except: return None

def salvar_questao(dados):
    try: return get_supabase().table("questionarios").insert(dados).execute()
    except: return None

def listar_flashcards(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("is_global", False).neq("categoria", "Lixeira").execute()
        return res.data if isinstance(res.data, list) else []
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

# --- 4. HISTÓRICO DE CONSULTAS ---
def salvar_historico_chat(email, pergunta, resposta, area, subtema):
    try: get_supabase().table("flashcards").insert({"pergunta": str(pergunta), "resposta": str(resposta), "grande_area": str(area), "subtema": str(subtema), "categoria": "Historico_Chat", "is_global": False, "criado_por_email": email}).execute()
    except: pass

def carregar_historico_chat(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Historico_Chat").order("id", desc=True).limit(10).execute()
        if res.data and isinstance(res.data, list): return [h for h in res.data if isinstance(h, dict)]
        return []
    except: return []

# --- 5. LIXEIRA / RECICLAGEM ---
def mover_para_lixeira(item_id):
    try: return get_supabase().table("flashcards").update({"categoria": "Lixeira", "is_global": False}).eq("id", item_id).execute()
    except: return False

def restaurar_da_lixeira(item_id):
    try: return get_supabase().table("flashcards").update({"categoria": "Resumo"}).eq("id", item_id).execute()
    except: return False

def esvaziar_lixeira(email):
    try: return get_supabase().table("flashcards").delete().eq("criado_por_email", email).eq("categoria", "Lixeira").execute()
    except: return False

def listar_lixeira(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Lixeira").execute()
        return res.data if isinstance(res.data, list) else []
    except: return []
