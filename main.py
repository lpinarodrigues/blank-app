import streamlit as st
from database import get_core_score

# 1. Configuração Master (Ocultando a sidebar padrão no mobile)
st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DE APP MODERNO (UI/UX 2026)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F1F5F9;
    }

    /* HEADER MODERNO */
    .app-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 20px;
        border-radius: 0 0 25px 25px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.2);
    }

    /* CARDS DE CONTEÚDO */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent;
    }
    
    .stMetric {
        background-color: white !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }

    /* BARRA DE NAVEGAÇÃO INFERIOR (ESTILO APP) */
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        display: flex;
        justify-content: space-around;
        padding: 12px 0;
        border-top: 1px solid #E2E8F0;
        z-index: 999999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    
    /* BOTÃO DE SAIR ESTILIZADO */
    .stButton>button {
        border-radius: 12px;
        border: none;
        background: #1E3A8A;
        color: white;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* REMOVER ELEMENTOS INÚTEIS DO STREAMLIT */
    header[data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Lógica de Autenticação
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'menu_atual' not in st.session_state:
    st.session_state.menu_atual = "📊 Dashboard"

# Importações Seguras
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
    from paginas.perfil import perfil_view
except ImportError:
    st.error("Sincronizando componentes...")

if not st.session_state.autenticado:
    login_view.show()
else:
    # HEADER DINÂMICO
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    score = get_core_score(email)
    st.markdown(f'''
        <div class="app-header">
            <h2 style="margin:0; font-size: 1.4rem;">🛡️ CORE NEXUS</h2>
            <p style="margin:5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">🏆 {score} pts | {email}</p>
        </div>
    ''', unsafe_allow_html=True)

    # BARRA DE NAVEGAÇÃO SUPERIOR (Botões Grandes como App)
    menu_selecionado = st.segmented_control(
        "Área de Atuação", 
        ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "👤 Perfil"],
        selection_mode="single",
        default=st.session_state.menu_atual
    )
    
    if menu_selecionado:
        st.session_state.menu_atual = menu_selecionado

    st.divider()

    # ROTEAMENTO DE CONTEÚDO
    if st.session_state.menu_atual == "📊 Dashboard":
        dashboard_view.show()
    elif st.session_state.menu_atual == "🧠 Core AI":
        core_ai_view.show()
    elif st.session_state.menu_atual == "📚 Master Study":
        estudo_ativo_view.show()
    elif st.session_state.menu_atual == "👤 Perfil":
        perfil_view.show()
        if st.button("🚪 Sair do Sistema", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

    # ESPAÇO FINAL PARA NÃO TAPAR O CONTEÚDO COM A BARRA (Se existisse nav fixa)
    st.write("<br><br>", unsafe_allow_html=True)
