import streamlit as st
from supabase import create_client

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Função de Inserção Padrão Ouro
def salvar_flashcard_estruturado(p, r, area, subtema, tema, email, exp="", nivel=2):
    get_supabase().table("flashcards").insert({
        "pergunta": p, 
        "resposta": r, 
        "grande_area": area,
        "subtema": subtema,
        "categoria": tema, # Mantido por compatibilidade
        "criado_por_email": email, 
        "explicacao": exp,
        "complexidade": nivel
    }).execute()

def salvar_questao_estruturada(dados):
    # Garante que os campos de hierarquia existam
    get_supabase().table("questionarios").insert(dados).execute()

def listar_temas_disponiveis():
    res = get_supabase().table("flashcards").select("grande_area, subtema").execute()
    return res.data
