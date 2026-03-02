import streamlit as st
import sys
import os

# Configuração de Página - ESTA É A CHAVE PARA O VISUAL
st.set_page_config(
    page_title="CORE NEXUS", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Injeção de CSS para o visual moderno (Azul e Branco Hospitalar)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1E3A8A; color: white; height: 3em; font-weight: bold; }
    .stRadio > label { font-weight: bold; color: #1E3A8A; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
""", unsafe_allow_html=True)

from paginas.login import login_view
from paginas.dashboard import dashboard_view
from paginas.core_ai import core_ai_view
from paginas.estudo_ativo import estudo_ativo_view

# Gerenciamento de Sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    # Barra Lateral Estilizada
    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center;'>🛡️ CORE NEXUS</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>👤 <b>{st.session_state.get('user_email', 'Médico')}</b></p>", unsafe_allow_html=True)
        st.divider()
        
        menu = st.radio("Navegação Principal:", ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "⚙️ Configurações"])
        
        st.spacer = st.container()
        st.write("") # Espaçador
        if st.button("🚪 Encerrar Sessão"):
            st.session_state.autenticado = False
            st.rerun()

    # Roteamento de Páginas
    if menu == "📊 Dashboard":
        dashboard_view.show()
    elif menu == "🧠 Core AI":
        core_ai_view.show()
    elif menu == "📚 Master Study":
        estudo_ativo_view.show()
    else:
        st.title("⚙️ Configurações")
        st.write("Ajustes de perfil e notificações.")
