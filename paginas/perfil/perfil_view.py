import streamlit as st

def show():
    st.title("👤 Meu Perfil")
    st.write(f"Usuário: {st.session_state.get('user_email', 'Visitante')}")
