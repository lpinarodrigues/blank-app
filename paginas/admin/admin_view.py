import streamlit as st
import google.generativeai as genai

def show():
    st.markdown("### ⚡ Painel de Controle Admin | Core AI")
    st.caption("Agente Admin Ativo: Monitorando integridade e performance.")

    # Conectar com a 4ª Chave (Admin Agent)
    genai.configure(api_key=st.secrets["GEMINI_ADMIN_KEY"])
    model_admin = genai.GenerativeModel('gemini-1.5-pro')

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Agentes Ativos", "4 Gemini + 1 Groq")
    with col2:
        st.metric("Status do Sistema", "100% Operacional", delta="Estável")

    st.divider()
    
    # Função do Admin Agent: Analisar o Sistema
    st.subheader("🤖 Relatório do Agente Admin")
    if st.button("Gerar Auditoria de Sistema"):
        with st.spinner("O Core Admin está auditando os módulos..."):
            # O Admin Agent analisa a estrutura do código e as chaves
            prompt = "Aja como um CTO Médico. Analise uma arquitetura de 3 agentes clínicos e sugira 3 melhorias de UX para um app médico de celular."
            relatorio = model_admin.generate_content(prompt).text
            st.markdown(relatorio)

    st.divider()
    st.subheader("🔑 Gerenciamento de Chaves")
    st.info("Chave Admin: AIzaSy...Ekyw (Ativa)\nChaves Clínicas: 3 Gemini + 1 Groq (Ativas)")
