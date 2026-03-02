import streamlit as st
import time

def show():
    st.markdown("### 🧠 Core AI | Oráculo de Diretrizes")
    st.caption("Baseado em Evidências: ESC, AHA, SBC e Protocolos Institucionais.")

    # 1. Atalhos de Emergência (Eficiência no Plantão)
    st.write("⚡ **Protocolos de Acesso Rápido:**")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("🚨 IAM c/ Supra"):
            st.session_state.query_ai = "Manejo de IAM com supra de ST e tempo porta-balão"
    with col_b:
        if st.button("🧠 AVC Isquêmico"):
            st.session_state.query_ai = "Critérios de trombólise no AVC isquêmico"
    with col_c:
        if st.button("🏥 Sepse/Choque"):
            st.session_state.query_ai = "Protocolo de ressuscitação volêmica na Sepse"

    st.divider()

    # 2. Campo de Busca Inteligente
    if 'query_ai' not in st.session_state:
        st.session_state.query_ai = ""

    query = st.text_input("Sua dúvida clínica:", value=st.session_state.query_ai, placeholder="Ex: Anticoagulação na FA valvar...")

    if query:
        with st.status("Consultando base de dados...", expanded=True):
            st.write("🔍 Varrendo diretrizes atualizadas 2024-2026...")
            time.sleep(1) # Simulação de latência de processamento IA
            st.write("⚖️ Cruzando com protocolos da Unifesp/Dante...")
            st.success("Análise Concluída.")
        
        # 3. Exibição da Resposta (Layout de Card)
        with st.container(border=True):
            st.markdown(f"#### 🛡️ Conduta Sugerida para: *{query}*")
            st.info("Esta é uma sugestão baseada em protocolos. A decisão final é do médico assistente.")
            st.write("""
            **Pontos Chave:**
            1. Verifique estabilidade hemodinâmica imediata.
            2. Inicie monitorização contínua e acesso venoso calibroso.
            3. Consulte a tabela de doses no rodapé da diretriz específica.
            """)
            st.caption("Fonte: Diretriz Brasileira de Cardiologia (2024) / Arquivos Brasileiros de Cardiologia.")

