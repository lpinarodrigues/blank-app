import streamlit as st
from supabase import create_client

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def get_core_score(email):
    try:
        res = get_supabase().table("membros_core").select("score").eq("email", email).execute()
        return res.data[0]['score'] if res.data else 0
    except: return 0

def obter_ranking_elite():
    try:
        supabase = get_supabase()
        res = supabase.table("resultados_performance").select("user_email, acertos, questoes_respondidas").execute()
        if not res.data: return []
        # Lógica de agregação simples
        stats = {}
        for r in res.data:
            e = r['user_email']
            if e not in stats: stats[e] = {"acertos": 0, "total": 0}
            stats[e]["acertos"] += r['acertos']
            stats[e]["total"] += r['questoes_respondidas']
        ranking = [{"email": k, "aproveitamento": round((v['acertos']/v['total']*100),1), "total": v['total']} for k, v in stats.items()]
        return sorted(ranking, key=lambda x: x['aproveitamento'], reverse=True)
    except: return []

def salvar_flashcard(p, r, cat, email, exp=""):
    get_supabase().table("flashcards").insert({
        "pergunta": p, "resposta": r, "categoria": cat, "criado_por_email": email, "explicacao": exp
    }).execute()

def listar_flashcards(email):
    res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).execute()
    return res.data if res.data else []

def atualizar_revisao_card(card_id, qualidade):
    # Simplificado para evitar erros de import de pandas aqui
    get_supabase().table("flashcards").update({"revisões_totais": 1}).eq("id", card_id).execute()
