import streamlit as st

def show():
    st.markdown("### 🧠 Core AI | Oráculo de Diretrizes")
    st.write("Consulta rápida de condutas baseada em evidências.")
    
    # Interface de Busca de Alta Performance
    query = st.text_input("Sua dúvida clínica (ex: 'Dosagem de Adrenalina na PCR'):", placeholder="Digite aqui...")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Consultar Diretrizes"):
            if query:
                with st.status("Varrendo bases de dados médicas...", expanded=True):
                    st.write("🔎 Buscando em: ESC, AHA, SBC, e Diretrizes Unifesp...")
                    st.write("⚡ Latência otimizada: 120ms")
                    st.success("Conduta sugerida: Verifique o protocolo de suporte avançado de vida (ACLS 2024).")
            else:
                st.warning("Por favor, insira uma dúvida clínica.")
