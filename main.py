import streamlit as st
from database import get_core_score

# Configuração de Elite (Sempre a primeira linha)
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# CSS Responsivo para Celular
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1E3A8A !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { border-radius: 8px; background-color: #1E3A8A; color: white; height: 3em; }
    @media (max-width: 768px) {
        .stMetric { background-color: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    }
    </style>
""", unsafe_allow_html=True)

# Lógica de Sessão e Cache
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# Importação das abas
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
except ImportError:
    st.error("Sincronizando módulos...")

if not st.session_state.autenticado:
    login_view.show()
else:
    with st.sidebar:
        st.markdown("# 🛡️ CORE NEXUS")
        # Mostra o Score direto na barra lateral (Engajamento)
        email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
        score = get_core_score(email)
        st.subheader(f"🏆 Score: {score}")
        st.divider()
        
        menu = st.radio("Menu", ["📊 Dashboard", "🧠 Core AI", "📚 Master Study"])
        
        if st.button("🚪 Sair"):
            st.session_state.autenticado = False
            st.rerun()

    # Roteamento Eficiente
    if menu == "📊 Dashboard": dashboard_view.show()
    elif menu == "🧠 Core AI": core_ai_view.show()
    elif menu == "📚 Master Study": estudo_ativo_view.show()
