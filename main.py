import streamlit as st
import sys
import os

# 1. CONFIGURAÇÃO DE LAYOUT (EXPANDE A TELA)
st.set_page_config(
    page_title="CORE NEXUS | Inteligência Médica",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. O DESIGN "DE CÉU PARA A TERRA" (CSS CUSTOMIZADO)
st.markdown("""
    <style>
    /* Fundo e Fonte Geral */
    .stApp {
        background-color: #F4F7F9;
    }
    
    /* Barra Lateral Azul Profundo */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Botões Estilo Hospitalar (Elite) */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A;
        color: white;
        height: 3em;
        font-weight: bold;
        border: 1px solid #ffffff33;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        border: 1px solid #ffffff;
    }
    
    /* Títulos e Cards */
    h1, h2, h3 {
        color: #1E3A8A;
        font-family: 'Inter', sans-serif;
    }
    
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Imports das Páginas
from paginas.login import login_view
from paginas.dashboard import dashboard_view
from paginas.core_ai import core_ai_view
from paginas.estudo_ativo import estudo_ativo_view

# Gestão de Sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    # Sidebar Estilizada
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: white;'>🛡️ CORE NEXUS</h1>", unsafe_allow_html=True)
        st.write(f"🟢 **Médico:** {st.session_state.get('user_email', 'Lucas Pina')}")
        st.divider()
        
        menu = st.radio(
            "Navegação:",
            ["📊 Dashboard", "🧠 Core AI (Oráculo)", "📚 Master Study", "👤 Meu Perfil"]
        )
        
        st.write("")
        if st.button("🚪 Sair do Sistema"):
            st.session_state.autenticado = False
            st.rerun()

    # Roteamento
    if menu == "📊 Dashboard":
        dashboard_view.show()
    elif menu == "🧠 Core AI (Oráculo)":
        core_ai_view.show()
    elif menu == "📚 Master Study":
        estudo_ativo_view.show()
    else:
        st.title("👤 Perfil do Utilizador")
        st.info("Configurações da conta e preferências de notificação.")

