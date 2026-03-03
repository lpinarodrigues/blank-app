import streamlit as st
import sys
import os

# Força o diretório raiz no PATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        from paginas.login import login_view
        login_view.show()
    except Exception as e:
        st.error(f"Erro ao carregar login: {e}")
else:
    with st.sidebar:
        st.title(f"🛡️ CORE NEXUS")
        menu = st.radio(
            "Navegação:",
            ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "📝 Simulados", "🚑 Plantão", "🛠️ Ferramentas"]
        )
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

    # Mapeamento Seguro
    try:
        if menu == "📊 Dashboard":
            from paginas.dashboard import dashboard_view
            dashboard_view.show()
        elif menu == "🧠 Core AI":
            from paginas.core_ai import core_ai_view
            core_ai_view.show()
        elif menu == "📚 Master Study":
            from paginas.estudo_ativo import estudo_ativo_view
            st.session_state.revelado = st.session_state.get('revelado', False)
            estudo_ativo_view.show()
        elif menu == "📝 Simulados":
            from paginas.simulados import simulados_view
            simulados_view.show()
        elif menu == "🚑 Plantão":
            from paginas.plantao import handoff_view
            handoff_view.show()
        elif menu == "🛠️ Ferramentas":
            from paginas.ferramentas import ferramentas_view
            ferramentas_view.show()
    except Exception as e:
        st.error(f"Erro na navegação: {e}")
        st.info("Verifique se todos os módulos foram carregados corretamente no servidor.")
