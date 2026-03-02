import streamlit as st
import sys
import os

# Forçar o Python a olhar a pasta atual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# CSS de Elite
st.markdown("<style>[data-testid='stSidebar'] {background-color: #1E3A8A; color: white;} .stButton>button {background-color: #1E3A8A; color: white; border-radius: 8px;}</style>", unsafe_allow_html=True)

# Inicialização segura das abas
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def carregar_aba(modulo, funcao="show"):
    try:
        import importlib
        mod = importlib.import_module(modulo)
        getattr(mod, funcao)()
    except Exception as e:
        st.error(f"Erro na aba {modulo}: {e}")
        st.info("Verifique se o arquivo existe na pasta 'paginas'.")

if not st.session_state.autenticado:
    carregar_aba("paginas.login.login_view")
else:
    with st.sidebar:
        st.title("🛡️ CORE NEXUS")
        st.write(f"👤 {st.session_state.get('user_email', 'Usuário')}")
        st.divider()
        menu = st.radio("Navegação", ["Dashboard", "Core AI", "Master Study", "Perfil"])
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

    if menu == "Dashboard": carregar_aba("paginas.dashboard.dashboard_view")
    elif menu == "Core AI": carregar_aba("paginas.core_ai.core_ai_view")
    elif menu == "Master Study": carregar_aba("paginas.estudo_ativo.estudo_ativo_view")
    elif menu == "Perfil": carregar_aba("paginas.perfil.perfil_view")
# Build Version: 1772459537
