import streamlit as st
from streamlit_cookies_controller import CookieController
from paginas.login import login_view
from paginas.dashboard import dashboard_view
from paginas.core_ai import core_ai_view
from paginas.estudo_ativo import estudo_ativo_view
from paginas.perfil import perfil_view

st.set_page_config(page_title="CORE NEXUS", page_icon="🛡️", layout="wide")

# Inicializa o controlador de cookies
controller = CookieController()

def show_app():
    # Tenta recuperar o login salvo nos cookies do navegador
    cookie_auth = controller.get('core_nexus_auth')
    
    if 'autenticado' not in st.session_state:
        if cookie_auth:
            st.session_state.autenticado = True
            st.session_state.user_email = cookie_auth
        else:
            st.session_state.autenticado = False

    if not st.session_state.autenticado:
        login_view.show()
        # Se o usuário logar dentro do login_view, precisamos salvar o cookie lá também
    else:
        with st.sidebar:
            st.title("🛡️ CORE NEXUS")
            st.write(f"👤 {st.session_state.get('user_email')}")
            st.divider()
            menu = st.radio("Navegação", ["Dashboard", "Core AI", "Master Study", "Meu Perfil"])
            
            if st.button("Sair"):
                controller.remove('core_nexus_auth')
                st.session_state.autenticado = False
                st.rerun()

        if menu == "Dashboard":
            dashboard_view.show()
        elif menu == "Core AI":
            core_ai_view.show()
        elif menu == "Master Study":
            estudo_ativo_view.show()
        else:
            perfil_view.show()

if __name__ == "__main__":
    show_app()
