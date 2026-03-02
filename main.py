import streamlit as st

# 1. FORÇAR O LAYOUT (Isso resolve o problema da sua imagem)
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# 2. INJETAR O DESIGN (Para tirar o branco e colocar o azul de elite)
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #1E3A8A !important; color: white !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { border-radius: 8px; background-color: #1E3A8A; color: white; }
    </style>
""", unsafe_allow_html=True)

# 3. Importação Segura
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
except ImportError:
    st.error("Reconectando módulos...")

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    with st.sidebar:
        st.markdown("# 🛡️ CORE NEXUS")
        menu = st.radio("Navegação", ["Dashboard", "Core AI", "Master Study", "Meu Perfil"])
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()

    if menu == "Dashboard": dashboard_view.show()
    elif menu == "Core AI": core_ai_view.show()
    elif menu == "Master Study": estudo_ativo_view.show()
