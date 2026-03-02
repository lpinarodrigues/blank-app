import streamlit as st
from paginas.login import login_view
from paginas.estudo import estudo_view
from paginas.estudo_ativo import estudo_ativo_view
from paginas.cronograma import cronograma_view
from paginas.scores import scores_view
from paginas.pharma import pharma_view
from paginas.pesquisa import laboratorio_view
from paginas.decisao import precision_view
from paginas.prontuario import prontuario_view
from paginas.perfil import perfil_view

st.set_page_config(page_title="CORE NEXUS", layout="wide", initial_sidebar_state="collapsed")

# --- CSS CORRIGIDO: BOTÕES COM CONTRASTE ALTO ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo dos Botões do Dashboard */
    .stButton>button {
        border-radius: 12px;
        height: 3.8em;
        font-weight: bold;
        background-color: #ffffff !important; /* Fundo Branco */
        color: #1E3A8A !important;           /* Texto Azul Escuro */
        border: 2px solid #1E3A8A !important; /* Borda Azul Escuro */
        transition: all 0.3s ease;
    }
    
    /* Efeito ao passar o mouse */
    .stButton>button:hover {
        background-color: #1E3A8A !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Home"

    # --- LÓGICA DE NAVEGAÇÃO ---
    try:
        if st.session_state.pagina == "Home":
            st.title("🚀 CORE NEXUS | Dashboard")
            st.subheader("Selecione sua área de atuação:")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🧠 Core AI (Oráculo)", use_container_width=True): 
                    st.session_state.pagina = "Core AI"; st.rerun()
                if st.button("📊 Core Scores", use_container_width=True): 
                    st.session_state.pagina = "Scores"; st.rerun()
            with c2:
                if st.button("📚 Master Study", use_container_width=True): 
                    st.session_state.pagina = "Master Study"; st.rerun()
                if st.button("💊 Core Pharma", use_container_width=True): 
                    st.session_state.pagina = "Pharma"; st.rerun()
            with c3:
                if st.button("📅 Cronograma", use_container_width=True): 
                    st.session_state.pagina = "Cronograma"; st.rerun()
                if st.button("🔬 Pesquisa/Lab", use_container_width=True): 
                    st.session_state.pagina = "Pesquisa"; st.rerun()

        # --- ROTEAMENTO ---
        elif st.session_state.pagina == "Core AI": estudo_view.show()
        elif st.session_state.pagina == "Master Study": estudo_ativo_view.show()
        elif st.session_state.pagina == "Scores": scores_view.show()
        elif st.session_state.pagina == "Pharma": pharma_view.show()
        elif st.session_state.pagina == "Cronograma": cronograma_view.show()
        elif st.session_state.pagina == "Pesquisa": laboratorio_view.show()
        elif st.session_state.pagina == "Perfil": perfil_view.show()

    except Exception as e:
        st.error(f"🚨 Autocura: Erro no módulo {st.session_state.pagina}. Retornando à Home...")
        st.session_state.pagina = "Home"

    # --- MENU INFERIOR FIXO (FOOTER) ---
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    if m1.button("🏠 Home", use_container_width=True): 
        st.session_state.pagina = "Home"; st.rerun()
    if m2.button("🔙 Voltar", use_container_width=True): 
        st.session_state.pagina = "Home"; st.rerun()
    if m3.button("👤 Perfil/ADM", use_container_width=True): 
        st.session_state.pagina = "Perfil"; st.rerun()
    if m4.button("🚪 Sair", use_container_width=True): 
        st.session_state.autenticado = False; st.rerun()
