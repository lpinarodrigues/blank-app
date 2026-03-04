import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, gerar_pdf_resposta, ler_arquivo_texto
from database import salvar_item_estudo, salvar_historico_chat, carregar_historico_chat, mover_para_lixeira

def show():
    st.markdown("### 🧠 Core AI | Terminal Clínico Avançado")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    with st.expander("📎 Anexar Documento Base (Opcional)", expanded=False):
        arquivo_upload = st.file_uploader("", type=["pdf", "docx", "txt"])

    pergunta = st.chat_input("Dúvida médica ou instrução...")
    dados_exibicao = None

    if pergunta:
        texto_extraido = ler_arquivo_texto(arquivo_upload) if arquivo_upload else ""
        with st.spinner("Processando..."):
            res, area, sub = consultar_core_ia_perfeicao(pergunta, texto_extraido)
            salvar_historico_chat(email, pergunta, res, area, sub)
            dados_exibicao = {"q": pergunta, "a": res, "area": area, "sub": sub}
    
    if dados_exibicao:
        with st.container(border=True):
            st.markdown(f"**Tema:** {dados_exibicao['q']}")
            st.markdown(dados_exibicao['a'])
            col1, col2, col3, col4 = st.columns(4)
            if col1.button("📥 Salvar Resumo"): salvar_item_estudo({"pergunta": dados_exibicao['q'], "resposta": dados_exibicao['a'], "grande_area": dados_exibicao['area'], "subtema": dados_exibicao['sub'], "categoria": "Resumo", "criado_por_email": email})
            if col2.button("🎴 Flashcards"): gerar_apenas_flashcards(dados_exibicao['a'], dados_exibicao['area'], dados_exibicao['sub'], email)
            if col3.button("📝 Questões"): gerar_apenas_questoes(dados_exibicao['a'], dados_exibicao['area'], dados_exibicao['sub'], email)
            pdf = gerar_pdf_resposta(dados_exibicao['a'], email)
            col4.download_button("📄 PDF", data=pdf, file_name="protocolo.pdf")
