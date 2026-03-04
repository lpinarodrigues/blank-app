import streamlit as st
from database import get_supabase, mover_para_lixeira

def show():
    st.markdown("### 📘 Meus Resumos")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").execute()
        resumos = [r for r in res.data if isinstance(r, dict)]
    except: resumos = []

    for r in resumos:
        with st.container(border=True):
            st.subheader(r.get('pergunta'))
            with st.expander("Ver Resumo"): st.markdown(r.get('resposta'))
            if st.button("🗑️", key=f"dr_{r['id']}"): mover_para_lixeira(r['id']); st.rerun()
