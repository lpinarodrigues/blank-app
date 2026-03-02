import streamlit as st

def show():
    st.title("💊 Core Pharma | Guia de Infusão")
    st.markdown("---")
    busca = st.text_input("🔍 Buscar Fármaco:")
    if busca.lower() == "noradrenalina":
        with st.container(border=True):
            st.subheader("💉 Noradrenalina (Nora)")
            col1, col2 = st.columns(2)
            col1.info("Diluição: 4 ampolas + 234ml SG5%")
            peso = col2.number_input("Peso (kg):", 40, 150, 70)
            vazao = col2.number_input("Vazão (ml/h):", 0.0, 50.0, 5.0)
            dose = (vazao * 64) / (peso * 60)
            st.metric("Dose (mcg/kg/min)", f"{dose:.3f}")
