import streamlit as st
from database import validar_login, cadastrar_membro

def show():
    st.markdown("## 🛡️ Acesso CORE NEXUS")
    
    tab1, tab2 = st.tabs(["Login", "Solicitar Acesso"])
    
    with tab1:
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = validar_login(email, senha)
            if user:
                st.session_state.autenticado = True
                st.session_state.user_email = email
                st.session_state.user_nome = user['nome']
                st.rerun()
            else:
                st.error("Usuário não encontrado ou aguardando aprovação.")
                
    with tab2:
        nome = st.text_input("Nome Completo")
        novo_email = st.text_input("E-mail Institucional")
        vinculo = st.selectbox("Vínculo", ["Residente", "Preceptor", "Staff", "Externo"])
        nova_senha = st.text_input("Definir Senha", type="password")
        if st.button("Enviar Solicitação"):
            cadastrar_membro(nome, novo_email, "", vinculo, nova_senha)
            st.success("Solicitação enviada! Aguarde aprovação do Admin.")
