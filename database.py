import streamlit as st
from supabase import create_client

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def validar_login(email, senha):
    supabase = get_supabase()
    res = supabase.table("membros_core").select("*").eq("email", email).eq("senha", senha).eq("aprovado", True).execute()
    return res.data[0] if res.data else None

def cadastrar_membro(nome, email, tel, vinculo, senha):
    supabase = get_supabase()
    return supabase.table("membros_core").insert({
        "nome": nome, "email": email, "tel": tel, "vinculo": vinculo, "senha": senha
    }).execute()

def salvar_questao_banco(dados):
    get_supabase().table("questionarios").insert(dados).execute()

def listar_questoes_simulado(categoria=None):
    supabase = get_supabase()
    query = supabase.table("questionarios").select("*")
    if categoria and categoria != "Geral":
        query = query.eq("categoria", categoria)
    res = query.order("created_at", desc=True).limit(10).execute()
    return res.data

def registrar_performance(email, respondidas, acertos):
    percent = (acertos / respondidas * 100) if respondidas > 0 else 0
    get_supabase().table("resultados_performance").insert({
        "user_email": email, "questoes_respondidas": respondidas, "acertos": acertos, "aproveitamento_percent": percent
    }).execute()

def obter_ranking_elite():
    supabase = get_supabase()
    # Puxa a performance agregada por usuário
    res = supabase.table("resultados_performance").select("user_email, acertos, questoes_respondidas").execute()
    if not res.data:
        return []
    
    # Agregação simples para o Ranking
    ranking = {}
    for r in res.data:
        email = r['user_email']
        if email not in ranking:
            ranking[email] = {"acertos": 0, "total": 0}
        ranking[email]["acertos"] += r['acertos']
        ranking[email]["total"] += r['questoes_respondidas']
    
    lista_ranking = []
    for email, dados in ranking.items():
        aproveitamento = (dados["acertos"] / dados["total"] * 100) if dados["total"] > 0 else 0
        lista_ranking.append({"email": email, "aproveitamento": round(aproveitamento, 1), "total": dados["total"]})
    
    return sorted(lista_ranking, key=lambda x: x['aproveitamento'], reverse=True)

def salvar_handoff(email, leito, quadro, sbar, flags):
    get_supabase().table("plantao_handoff").insert({
        "medico_email": email,
        "paciente_leito": leito,
        "quadro_clinico": quadro,
        "sbar_json": sbar,
        "red_flags": flags
    }).execute()

def listar_ultimos_handoffs():
    return get_supabase().table("plantao_handoff").select("*").order("created_at", desc=True).limit(10).execute().data
