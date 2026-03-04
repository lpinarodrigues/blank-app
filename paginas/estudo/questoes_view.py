import streamlit as st
from database import listar_questoes

def show():
    st.markdown("### 📝 Simulados")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    qs = listar_questoes(email)
    for i, q in enumerate(qs):
        with st.container(border=True):
            st.write(f"**{i+1}. {q.get('pergunta')}**")
            st.write(f"A) {q.get('opcao_a')}")
            st.write(f"B) {q.get('opcao_b')}")
            with st.expander("Gabarito"): st.success(q.get('gabarito'))
