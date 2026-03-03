import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_pdf_resposta, gerar_batch_flashcards
from database import salvar_item_estudo

def show():
    st.markdown("### 🧠 Core AI | Consultoria e Documentação")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    pergunta = st.chat_input("Dúvida clínica ou conduta...")
    
    if pergunta:
        resposta, info = consultar_core_ia_perfeicao(pergunta)
        
        # --- AUTO-SAVE NA ABA DE RESUMOS ---
        resumo_data = {
            "pergunta": f"RESUMO: {pergunta}",
            "resposta": resposta[:500] + "...", # Versão curta para o card de resumo
            "grande_area": "Clínica Médica",
            "subtema": "Auto-Gerado via Core AI",
            "is_global": False,
            "criado_por_email": email
        }
        salvar_item_estudo(resumo_data)
        st.toast("✅ Resumo técnico salvo na sua biblioteca!")
        
        st.session_state.ultima_resposta = resposta
        st.markdown(resposta)
        
        col1, col2, col3 = st.columns(3)
        
        # Botão PDF
        pdf_file = gerar_pdf_resposta(resposta)
        col1.download_button("📄 Baixar PDF", data=pdf_file, file_name="conduta_nexus.pdf", mime="application/pdf")
        
        # Botão Flashcards
        if col2.button("🎴 Gerar 15 Itens"):
            total = gerar_batch_flashcards(resposta, pergunta[:20], email)
            st.success(f"{total} itens gerados!")
            
        col3.button("🔄 Nova Consulta")
