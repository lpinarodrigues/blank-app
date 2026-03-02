import streamlit as st
import sys
import os

# 1. Configuração de Base (Essencial para abrir em qualquer dispositivo)
st.set_page_config(
    page_title="CORE NEXUS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Design de Elite (CSS para garantir o visual azul e profissional)
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #1E3A8A !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #1E3A8A; 
        color: white; 
        font-weight: bold;
        border: 1px solid #ffffff33;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Importação das Páginas (As ligações que você pediu)
# Importamos os módulos que já possuem o código original
try:
    from paginas.login import login_view
    from paginas.dashboard import dashboard_view
    from paginas.core_ai import core_ai_view
    from paginas.estudo_ativo import estudo_ativo_view
    from paginas.perfil import perfil_view
except ImportError as e:
    st.error(f"Erro ao localizar uma das pastas: {e}")

# 4. Lógica de Navegação
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    login_view.show()
else:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🛡️ CORE NEXUS</h2>", unsafe_allow_html=True)
        st.write(f"🟢 **Médico:** {st.session_state.get('user_email', 'Usuário')}")
        st.divider()
        
        # Aqui criamos os links diretos para cada página
        menu = st.radio(
            "Selecione a Área:",
            ["📊 Dashboard", "🧠 Core AI", "📚 Master Study", "👤 Meu Perfil"]
        )
        
        st.write("")
        if st.button("🚪 Sair"):
            st.session_state.autenticado = False
            st.rerun()

    # 5. O "Direcionador" (Chama o código que já está nas pastas)
    if menu == "📊 Dashboard":
        dashboard_view.show()
    elif menu == "🧠 Core AI":
        core_ai_view.show()
    elif menu == "📚 Master Study":
        estudo_ativo_view.show()
    elif menu == "👤 Meu Perfil":
        perfil_view.show()
