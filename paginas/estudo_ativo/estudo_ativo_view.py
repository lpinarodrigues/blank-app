import streamlit as st

def show():
    st.markdown("### 📚 Master Study | Estudo Ativo")
    st.write("Selecione o Deck de Flashcards:")
    deck = st.selectbox("Especialidade", ["Cardiologia", "Clínica Médica", "UTI"])
    if st.button("Iniciar Sessão de Revisão"):
        st.warning(f"Carregando deck de {deck}...")
