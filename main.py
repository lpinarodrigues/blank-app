import streamlit as st
import sys
import os

# 1. Manter o Layout Wide e Visual (O que você já tinha)
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# CSS Original para manter o Design de Elite
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #1E3A8A; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1E3A8A; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Reconexão dos Módulos (Aba por Aba)
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
    from paginas.perfil import perfil_view
except ImportError as e:
    st.error(f"Erro ao conectar abas: {e}")

# 3. Lógica de Sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# 4. Roteamento das Abas
if not st.session_state.autenticado:
    login_view.show()
else:
    with st.sidebar:
        st.markdown("# 🛡️ CORE NEXUS")
        st.write(f"👤 {st.session_state.get('user_email', 'Médico')}")
        st.divider()
        
        # O Menu que reconecta tudo
        menu = st.radio(
            "Navegação", 
            ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "👤 Meu Perfil"]
        )
        
        st.write("")
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

    # Execução do código original de cada aba
    if menu == "📊 Dashboard":
        dashboard_view.show()
    elif menu == "🧠 Core AI":
        core_ai_view.show()
    elif menu == "📚 Master Study":
        estudo_ativo_view.show()
    elif menu == "👤 Meu Perfil":
        perfil_view.show()
