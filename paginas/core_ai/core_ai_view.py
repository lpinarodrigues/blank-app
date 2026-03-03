import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, gerar_pdf_resposta
from database import salvar_item_estudo

def show():
    st.markdown("### 🧠 Core AI | Terminal Clínico e Gerador de Estudos")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    pergunta = st.chat_input("Insira o tema, caso clínico ou dúvida médica...")
    
    if pergunta:
        with st.spinner("Estruturando resposta e extraindo tags (Área/Subtema)..."):
            resposta, area, subtema = consultar_core_ia_perfeicao(pergunta)
            
            # 1. AUTO-SAVE NA ABA DE RESUMOS COM AS TAGS CORRETAS
            resumo_db = {
                "pergunta": f"Resumo Oficial: {pergunta}",
                "resposta": resposta,
                "grande_area": area,
                "subtema": subtema,
                "categoria": "Resumo",
                "is_global": True,
                "criado_por_email": email
            }
            salvar_item_estudo(resumo_db)
            st.toast(f"✅ Auto-Resumo salvo na Global em: {area} > {subtema}")
            
            st.session_state.chat_history.append({
                "q": pergunta, "a": resposta, "area": area, "subtema": subtema
            })

    # Mostrar o Histórico com os Botões e Resultados VISÍVEIS
    for i, chat in enumerate(st.session_state.chat_history):
        with st.container(border=True):
            st.markdown(f"**Tema:** {chat['q']}")
            st.markdown(chat['a'])
            st.caption(f"🏷️ Classificação Automática: **{chat['area']} | {chat['subtema']}**")
            
            st.divider()
            st.write("🛠️ **Transformar este conhecimento:**")
            col1, col2, col3 = st.columns(3)
            
            # Ação 1: Flashcards
            if col1.button("🎴 Gerar Flashcards", key=f"btn_f_{i}"):
                with st.spinner("Criando flashcards..."):
                    cards = gerar_apenas_flashcards(chat['a'], chat['area'], chat['subtema'], email)
                    if cards:
                        st.success(f"✅ {len(cards)} Flashcards salvos em '{chat['subtema']}' (Global).")
                        for c in cards:
                            st.info(f"**Q:** {c['p']}\n\n**R:** {c['r']}") # MOSTRA NA TELA
                    else: st.error("Erro ao gerar.")
            
            # Ação 2: Questões
            if col2.button("📝 Gerar Questões", key=f"btn_q_{i}"):
                with st.spinner("Montando simulado..."):
                    questoes = gerar_apenas_questoes(chat['a'], chat['area'], chat['subtema'], email)
                    if questoes:
                        st.success(f"✅ {len(questoes)} Questões enviadas para o Banco de Elite.")
                        for q in questoes:
                            st.warning(f"**Questão:** {q['pergunta']}\n\nA) {q['a']}\nB) {q['b']}\nC) {q['c']}\nD) {q['d']}\n\n✅ **Gabarito:** {q['gabarito']}\n💡 **Justificativa:** {q['justificativa']}") # MOSTRA NA TELA
                    else: st.error("Erro ao gerar.")
            
            # Ação 3: Baixar PDF
            pdf_data = gerar_pdf_resposta(chat['a'])
            col3.download_button("📄 Baixar PDF do Resumo", data=pdf_data, file_name=f"Resumo_Nexus_{i}.pdf", mime="application/pdf", key=f"btn_pdf_{i}")
