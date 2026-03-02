import streamlit as st
from database import get_core_score

# 1. Configuração Master
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DE ALTA USABILIDADE (Mobile-First)
st.markdown("""
    <style>
    /* Estilo Geral */
    .stApp { background-color: #F8FAFC; }
    
    /* BARRA LATERAL (AZUL PROFUNDO) */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
        min-width: 85vw !important; /* Ocupa quase tudo no celular */
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* MENU DE RÁDIO (TRANSFORMADO EM BOTÕES GIGANTES NO MOBILE) */
    div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px !important;
        margin-bottom: 12px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    /* BOTÃO DE SAIR (DESTAQUE NO RODAPÉ) */
    .stButton>button {
        height: 3.5rem;
        border-radius: 10px;
        font-weight: bold;
    }

    /* CABEÇALHO FIXO PARA CELULAR */
    @media (max-width: 768px) {
        .mobile-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: #1E3A8A;
            color: white;
            padding: 10px;
            text-align: center;
            z-index: 999;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .stApp { padding-top: 50px !important; }
        
        /* Instrução Visual */
        .instruction {
            background: #E0E7FF;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            font-size: 0.9rem;
            color: #1E3A8A;
            margin-bottom: 20px;
            font-weight: bold;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Lógica de Autenticação
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# Importações Seguras
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
except ImportError:
    st.error("Carregando módulos...")

if not st.session_state.autenticado:
    login_view.show()
else:
    # Cabeçalho Mobile
    st.markdown('<div class="mobile-header">🛡️ CORE NEXUS MOBILE</div>', unsafe_allow_html=True)
    st.markdown('<div class="instruction">👈 Toque na SETA no canto superior para abrir o MENU</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🛡️ MENU CORE</h2>", unsafe_allow_html=True)
        email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
        score = get_core_score(email)
        st.markdown(f"<p style='text-align: center;'>🏆 <b>Score: {score} pts</b></p>", unsafe_allow_html=True)
        st.divider()
        
        menu = st.radio("Selecione a Área:", ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "👤 Perfil"])
        
        st.write("")
        if st.button("🚪 Sair do Sistema"):
            st.session_state.autenticado = False
            st.rerun()

    # Roteamento
    if menu == "📊 Dashboard": dashboard_view.show()
    elif menu == "🧠 Core AI": core_ai_view.show()
    elif menu == "📚 Master Study": estudo_ativo_view.show()
    elif menu == "👤 Perfil":
        from paginas.perfil import perfil_view
        perfil_view.show()
