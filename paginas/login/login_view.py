import streamlit as st
from streamlit_cookies_controller import CookieController
from supabase import create_client

controller = CookieController()
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")
supabase = create_client(url, key)

def show():
    st.title("🛡️ Acesso CORE NEXUS")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        # Login mestre para o Lucas
        if email == "lucas.pina@unifesp.br" and senha == "Med737230":
            controller.set('core_nexus_auth', email) # Salva no navegador!
            st.session_state.autenticado = True
            st.session_state.user_email = email
            st.rerun()
        else:
            res = supabase.table("membros_core").select("*").eq("email", email).eq("senha", senha).eq("aprovado", True).execute()
            if res.data:
                controller.set('core_nexus_auth', email)
                st.session_state.autenticado = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Acesso negado ou aguardando aprovação.")
