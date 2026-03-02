import streamlit as st
from database import update_score

def show():
    st.markdown("### 📚 Master Study | Estudo Ativo")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    st.info("Flashcard: Qual a primeira conduta na Taquicardia Ventricular sem Pulso?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Acertei (Ganhar +10 pts)"):
            novo = update_score(email, 10)
            st.success(f"Boa! Novo Score: {novo}")
            st.balloons()
    with col2:
        if st.button("❌ Errei (Revisar em 5 min)"):
            st.warning("Sem problemas. Vamos revisar em breve!")
