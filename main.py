import streamlit as st

# Configuração de Página para Mobile-First
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="centered")

# Inicialização de Estados de Sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    from paginas.login import login_view
    login_view.show()
else:
    # Menu Lateral Estilizado
    with st.sidebar:
        st.title(f"Olá, {st.session_state.get('user_nome', 'Doutor')}")
        menu = st.radio(
            "Navegação:",
            ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "📝 Simulados", "🚑 Plantão", "🛠️ Ferramentas"]
        )
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

    # Roteamento de Páginas com Indentação Corrigida
    if menu == "📊 Dashboard":
        from paginas.dashboard import dashboard_view
        dashboard_view.show()
    
    elif menu == "🧠 Core AI":
        from paginas.core_ai import core_ai_view
        core_ai_view.show()
    
    elif menu == "📚 Master Study":
        from paginas.estudo_ativo import estudo_ativo_view
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
