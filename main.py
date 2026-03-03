import streamlit as st
from database import get_core_score

st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# Lógica de Autenticação e Menu Restrito
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# Definir opções de menu baseadas no usuário
user_email = st.session_state.get('user_email', '')
if user_email == 'lucas.pina@unifesp.br' or user_email == 'lucas.pina@gmail.br':
    opcoes = ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "📝 Simulados", "👤 Perfil", "⚡ Admin"]
else:
    opcoes = ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "📝 Simulados", "👤 Perfil"]

if not st.session_state.autenticado:
    from paginas.login import login_view
    login_view.show()
else:
    # Header Moderno
    score = get_core_score(user_email)
    st.markdown(f'<div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); padding: 20px; border-radius: 0 0 25px 25px; color: white; text-align: center;"><h2>🛡️ CORE NEXUS</h2><p>🏆 {score} pts | {user_email}</p></div>', unsafe_allow_html=True)

    menu = st.segmented_control("Navegação", opcoes, selection_mode="single", default="📊 Dashboard")

    if menu == "📊 Dashboard": 
        from paginas.dashboard import dashboard_view
        dashboard_view.show()
    elif menu == "🧠 Core AI": 
        from paginas.core_ai import core_ai_view
        core_ai_view.show()
    elif menu == "📚 Master Study": 
    elif menu == "📝 Simulados":
        from paginas.simulados import simulados_view
        simulados_view.show()
        from paginas.estudo_ativo import estudo_ativo_view
        estudo_ativo_view.show()
    elif menu == "👤 Perfil": 
        from paginas.perfil import perfil_view
        perfil_view.show()
    elif menu == "⚡ Admin":
        from paginas.admin import admin_view
        admin_view.show()

    if st.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()
