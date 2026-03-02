import streamlit as st
from paginas.login import login_view
from paginas.dashboard import dashboard_view
from paginas.core_ai import core_ai_view
from paginas.estudo_ativo import estudo_ativo_view

st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# CSS de Elite
st.markdown("<style>[data-testid='stSidebar'] {background-color: #1E3A8A; color: white;} .stButton>button {background-color: #1E3A8A; color: white; border-radius: 8px;}</style>", unsafe_allow_html=True)

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
