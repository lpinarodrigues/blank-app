import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, gerar_pdf_resposta
from database import salvar_item_estudo

def show():
    st.markdown("### 🧠 Core AI | Terminal Clínico Avançado")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    pergunta = st.chat_input("Insira o tema, caso clínico ou dúvida médica...")
    
    if pergunta:
        with st.spinner("Estruturando resposta aprofundada e formatando referências (Vancouver)..."):
            resposta, area, subtema = consultar_core_ia_perfeicao(pergunta)
            
            # Auto-Save do Resumo
            salvar_item_estudo({
                "pergunta": f"Resumo Oficial: {pergunta}",
                "resposta": resposta,
                "grande_area": area,
                "subtema": subtema,
                "categoria": "Resumo",
                "is_global": True,
                "criado_por_email": email
            })
            
            st.session_state.chat_history.append({"q": pergunta, "a": resposta, "area": area, "subtema": subtema})

    for i, chat in enumerate(st.session_state.chat_history):
        with st.container(border=True):
            st.markdown(f"**Tema:** {chat['q']}")
            st.markdown(chat['a'])
            st.caption(f"🏷️ Classificação: **{chat['area']} | {chat['subtema']}**")
            
            st.divider()
            col1, col2, col3 = st.columns(3)
            
            if col1.button("🎴 Extrair Flashcards", key=f"btn_f_{i}"):
                with st.spinner("Minerando dados..."):
                    qtd = gerar_apenas_flashcards(chat['a'], chat['area'], chat['subtema'], email)
                    if qtd > 0: st.success(f"✅ {qtd} Flashcards salvos!")
                    else: st.error("Falha ao gerar flashcards.")
            
            if col2.button("📝 Extrair Questões", key=f"btn_q_{i}"):
                with st.spinner("Montando questões..."):
                    qtd = gerar_apenas_questoes(chat['a'], chat['area'], chat['subtema'], email)
                    if qtd > 0: st.success(f"✅ {qtd} Questões salvas!")
                    else: st.error("Falha ao gerar questões.")
            
            pdf_data = gerar_pdf_resposta(chat['a'], email)
            col3.download_button("📄 Baixar PDF Rastreado", data=pdf_data, file_name=f"Protocolo_{i}.pdf", mime="application/pdf", key=f"btn_pdf_{i}")
