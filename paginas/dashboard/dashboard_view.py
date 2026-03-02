import streamlit as st
from database import get_core_score

def show():
    st.markdown("### 📊 Painel de Performance Médica")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    # Busca o Score Real no Supabase
    score_real = get_core_score(email)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Core Score", f"{score_real} pts", "+15")
    with c2:
        st.metric("Retenção", "94%", "2%")
    with c3:
        st.metric("Meta Diária", "12/15", "80%")
