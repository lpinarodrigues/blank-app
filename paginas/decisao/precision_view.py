import streamlit as st

def show():
    st.title("🎯 Core Precision | Suporte Decisório")
    st.markdown("---")
    st.subheader("🧠 Heart Team Digital")
    with st.container(border=True):
        st.write("Análise de Risco")
        idade = st.slider("Idade:", 18, 100, 75)
        if st.button("⚖️ Consultar Diretrizes"):
            if idade > 75:
                st.success("Sugestão: TAVI.")
            else:
                st.info("Sugestão: Cirurgia Convencional.")
