import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_batch_flashcards

def show():
    st.markdown("### 🧠 Core AI | Consultoria de Elite")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    pergunta = st.chat_input("Dúvida clínica, escore ou conduta...")
    
    if pergunta:
        resposta, info = consultar_core_ia_perfeicao(pergunta)
        st.session_state.chat_history.append({"q": pergunta, "a": resposta, "info": info})

    for chat in st.session_state.chat_history[::-1]:
        with st.chat_message("user"):
            st.write(chat['q'])
        with st.chat_message("assistant"):
            st.markdown(chat['a'])
            st.caption(chat['info'])
            
            col1, col2 = st.columns(2)
            if col1.button("📥 Gerar 15 Itens (Flashcards/Questões)", key=f"gen_{chat['q'][:10]}"):
                email = st.session_state.get('user_email', 'admin@nexus.com')
                total = gerar_batch_flashcards(chat['a'], chat['q'][:20], email)
                if total > 0:
                    st.success(f"🎉 {total} itens enviados para o Master Study!")
                else:
                    st.error("Falha ao gerar itens. Verifique o formato JSON.")
