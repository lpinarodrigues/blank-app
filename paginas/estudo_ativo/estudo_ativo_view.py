import streamlit as st

def show():
    st.markdown("### 📚 Master Study | Revisão Espaçada")
    st.write("Sistema de estudo ativo para retenção de longo prazo.")
    
    # Seletor de Decks Eficiente
    deck = st.selectbox("Escolha o Deck de Revisão:", ["Cardiologia Clínica", "ECG de Alta Complexidade", "Emergências Médicas"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Flashcards para Hoje", "15", delta="Novo recorde")
    with col_b:
        st.metric("Precisão Média", "92%", delta="2%")
    
    st.divider()
    if st.button("🚀 Iniciar Sessão de Estudo"):
        st.info(f"Carregando deck: {deck}")
