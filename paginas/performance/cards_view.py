import streamlit as st
from shared_logic import chamar_oraculo

def show():
    st.title("🎓 Fábrica de Cards | Active Recall")
    st.markdown("---")

    # Verifica se há conteúdo vindo do Oráculo
    conteudo_bruto = st.session_state.get("card_temp", "")

    if not conteudo_bruto:
        st.info("💡 Dica: No Oráculo, clique em '🗂️ Flashcard' para enviar uma conduta para cá automaticamente.")
        texto_para_processar = st.text_area("Ou cole um texto médico aqui para gerar um card manual:")
    else:
        st.success("📥 Conteúdo recebido do Oráculo!")
        texto_para_processar = st.text_area("Refine o conteúdo se necessário:", value=conteudo_bruto, height=150)

    if st.button("✨ Gerar Flashcard Master"):
        if texto_para_processar:
            with st.spinner("IA estruturando Frente e Verso (Padrão Anki)..."):
                prompt_card = f"""
                Transforme o seguinte conteúdo médico em um flashcard de elite:
                {texto_para_processar}
                
                Formato de Saída:
                FRENTE: (Pergunta clínica desafiadora ou mnemônico incompleto)
                VERSO: (Resposta direta, Classe de Evidência e 'Pulo do Gato')
                """
                card_gerado = chamar_oraculo(prompt_card)
                
                # Exibição Visual do Card
                st.markdown("### 🎴 Seu Novo Card:")
                st.info(card_gerado)
                
                st.download_button("📥 Exportar para Anki (.txt)", 
                                 data=card_gerado, 
                                 file_name="nexus_card.txt", 
                                 mime="text/plain")
        else:
            st.warning("Insira algum conteúdo para gerar o card.")

