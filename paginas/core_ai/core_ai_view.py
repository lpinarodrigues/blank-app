import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_batch_flashcards

def show():
    st.markdown("### 🧠 Core AI | Oráculo & Conector")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')

    with st.container(border=True):
        query = st.text_input("Dúvida Clínica/Cirúrgica:", placeholder="Ex: Conduta na Colecistite Aguda...")
        if st.button("Consultar e Gerar Estudo ⚡", use_container_width=True):
            resposta, status = consultar_core_ia_perfeicao(query)
            st.session_state.ultima_resposta_longa = resposta
            st.markdown(resposta)
            
            # O BOTÃO MÁGICO DE CONEXÃO
            if st.button(f"📥 Gerar 15 Flashcards de {query}"):
                qtd = gerar_batch_flashcards(st.session_state.ultima_resposta_longa, query, email)
                st.success(f"Sucesso! {qtd} flashcards injetados no Master Study.")
