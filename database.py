import streamlit as st
from supabase import create_client
import pandas as pd

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def salvar_item_estudo(dados):
    try: return get_supabase().table("flashcards").insert(dados).execute()
    except: return None

def salvar_questao(dados):
    try: return get_supabase().table("questionarios").insert(dados).execute()
    except: return None

# --- HISTÓRICO BLINDADO CONTRA ERROS DE TIPO ---
def salvar_historico_chat(email, pergunta, resposta, area, subtema):
    try:
        get_supabase().table("flashcards").insert({
            "pergunta": str(pergunta), "resposta": str(resposta), "grande_area": str(area), 
            "subtema": str(subtema), "categoria": "Historico_Chat", "is_global": False, "criado_por_email": email
        }).execute()
    except: pass

def carregar_historico_chat(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Historico_Chat").order("id", desc=True).limit(10).execute()
        # Blindagem: Garante que retorna uma lista de dicionários
        if res.data and isinstance(res.data, list):
            return [h for h in res.data if isinstance(h, dict)]
        return []
    except: return []

# --- MOTOR DA LIXEIRA (RECICLAGEM) ---
def mover_para_lixeira(item_id):
    """Muda a categoria do item para Lixeira (Soft Delete)"""
    try:
        get_supabase().table("flashcards").update({"categoria": "Lixeira", "is_global": False}).eq("id", item_id).execute()
        return True
    except: return False

def restaurar_da_lixeira(item_id):
    """Restaura o item para o estado padrão"""
    try:
        get_supabase().table("flashcards").update({"categoria": "Resumo"}).eq("id", item_id).execute()
        return True
    except: return False

def esvaziar_lixeira(email):
    """Elimina definitivamente todos os itens da lixeira (Hard Delete)"""
    try:
        get_supabase().table("flashcards").delete().eq("criado_por_email", email).eq("categoria", "Lixeira").execute()
        return True
    except: return False

def listar_lixeira(email):
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Lixeira").execute()
        return res.data if isinstance(res.data, list) else []
    except: return []

def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        if res.data and isinstance(res.data, list) and isinstance(res.data[0], dict):
            return res.data[0].get('score', 0)
        return 0
    except: return 0
