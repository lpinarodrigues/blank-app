import streamlit as st

def show():
    st.title("📊 Core Scores | Calculadoras de Elite")
    st.caption("⚡ Motor de Decisão Ativo")
    st.markdown("---")
    try:
        servico = st.sidebar.radio("Especialidade:", ["Cardiologia", "Emergência/UTI"])
        if servico == "Cardiologia":
            score = st.selectbox("Escolha o Score:", ["GRACE", "CHA2DS2-VASc"])
            with st.container(border=True):
                st.subheader(f"Escore: {score}")
                st.info("Insira os dados clínicos.")
    except Exception as e:
        st.error("🚨 Falha no módulo. Autocura em ação...")
