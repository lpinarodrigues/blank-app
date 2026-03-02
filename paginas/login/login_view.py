import streamlit as st
from supabase import create_client, Client

# Configurações do seu Supabase
url: str = "https://svejzpsygmjgscjwwmzz.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2ZWp6cHN5Z21qZ3Njand3bXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzNzgyNzMsImV4cCI6MjA4Njk1NDI3M30.3UnmqMgRG01vEo2LT3hSTuIlqzUZw_DVHolj6l_hALM"
supabase: Client = create_client(url, key)

def show():
    st.title("🛡️ CORE NEXUS | Inteligência Médica")
    aba_acesso = st.tabs(["Acesso ao Sistema", "Solicitar Cadastro", "Recuperar Senha"])

    # --- LOGIN ---
    with aba_acesso[0]:
        u_email = st.text_input("E-mail:", key="l_email")
        u_pw = st.text_input("Senha:", type="password", key="l_pw")
        
        if st.button("Entrar no CORE", use_container_width=True):
            # LOGIN MASTER (BACKDOOR SEGURO)
            if u_email == "lucas.pina@unifesp.br" and u_pw == "Med737230":
                st.session_state.autenticado = True
                st.session_state.user_email = u_email
                st.session_state.is_adm = True
                st.rerun()
            else:
                # BUSCA NO BANCO DE DADOS REAL
                try:
                    res = supabase.table("usuarios").select("*").eq("email", u_email).eq("senha", u_pw).execute()
                    if res.data and res.data[0]['aprovado']:
                        st.session_state.autenticado = True
                        st.session_state.user_email = u_email
                        st.session_state.is_adm = False
                        st.rerun()
                    elif res.data and not res.data[0]['aprovado']:
                        st.warning("Seu acesso ainda está aguardando homologação do ADM.")
                    else:
                        st.error("Usuário ou senha incorretos.")
                except Exception as e:
                    st.error("Erro de conexão com o servidor central.")

    # --- CADASTRO ---
    with aba_acesso[1]:
        st.subheader("Solicitação de Credenciamento")
        nome = st.text_input("Nome Completo:")
        email = st.text_input("E-mail Profissional:")
        tel = st.text_input("Telefone:")
        vinculo = st.selectbox("Vínculo:", ["Residente", "Preceptor", "Interno", "Pesquisador"])
        senha = st.text_input("Definir Senha:", type="password")
        
        st.divider()
        st.markdown("### 📜 Termo de Consentimento e Responsabilidade (TCRT)")
        with st.container(border=True, height=250):
            st.markdown("O CORE NEXUS utiliza IA para suporte à decisão. É proibida a inserção de dados nominais de pacientes (LGPD/Lei 13.709/18). A responsabilidade final é do médico logado (Resolução CFM 2.217/18).")
        
        c1 = st.checkbox("Aceito o Termo de Responsabilidade.")
        c2 = st.checkbox("Ciente das obrigações da LGPD.")

        if st.button("Submeter Solicitação", use_container_width=True):
            if nome and email and senha and c1 and c2:
                try:
                    data = {
                        "nome": nome, "email": email, "tel": tel, 
                        "vinculo": vinculo, "senha": senha, "aprovado": False
                    }
                    supabase.table("usuarios").insert(data).execute()
                    st.success(f"Solicitação enviada com sucesso! Aguarde a validação do administrador.")
                except Exception as e:
                    st.error("Este e-mail já está cadastrado ou houve falha na rede.")
            else:
                st.error("Preencha todos os campos e aceite os termos.")
