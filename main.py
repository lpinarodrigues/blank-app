import streamlit as st
import sys
import os

# Configuração de Layout (Primeira linha sempre!)
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# CSS de Elite
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1E3A8A !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Importação das abas que acabamos de conferir
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
except ImportError as e:
    st.error(f"Erro de conexão: {e}")

# Lógica de Sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    with st.sidebar:
        st.title("🛡️ CORE NEXUS")
        menu = st.radio("Navegação", ["📊 Dashboard", "🧠 Core AI", "📚 Master Study"])
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

    if menu == "📊 Dashboard": dashboard_view.show()
    elif menu == "🧠 Core AI": core_ai_view.show()
    elif menu == "📚 Master Study": estudo_ativo_view.show()
