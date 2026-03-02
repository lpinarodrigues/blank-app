import streamlit as st
from shared_logic import registrar_aceite_lgpd
def show():
    st.header("⚖️ Segurança de Dados e Ética (LGPD)")
    st.info("Este sistema é uma ferramenta de suporte. Dados sensíveis de pacientes não devem ser inseridos.")
    if st.button("Aceito os Termos e Deveres"):
        registrar_aceite_lgpd(st.session_state.user_email)
        st.rerun()
