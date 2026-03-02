import streamlit as st

def show():
    st.markdown("### 🧠 Core AI | Oráculo de Diretrizes")
    st.write("Digite sua dúvida clínica baseada em evidências:")
    duvida = st.text_input("Ex: Qual o tempo porta-balão ideal?")
    if duvida:
        st.success(f"Analisando bases de dados para: {duvida}")
        st.write("⏱️ Processando resposta via latência otimizada...")
