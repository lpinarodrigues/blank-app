import streamlit as st
import sys
import os

# 1. Configuração de Layout (O que faz o app "aparecer")
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# 2. Injeção de CSS para o Visual Profissional
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #1E3A8A; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1E3A8A; color: white; border: 2px solid #ffffff; }
    h1, h2, h3 { color: #1E3A8A; }
    </style>
""", unsafe_allow_html=True)

# Imports de Segurança
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
except ImportError:
    st.error("Erro de sincronização de ficheiros. A reiniciar módulos...")

# Lógica de Autenticação
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    with st.sidebar:
        st.markdown("# 🛡️ CORE NEXUS")
        st.write(f"Médico: {st.session_state.get('user_email', 'Lucas')}")
        st.divider()
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()
    
    dashboard_view.show()
