import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, gerar_pdf_resposta, ler_arquivo_texto
from database import salvar_item_estudo, salvar_historico_chat, carregar_historico_chat, mover_para_lixeira

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    with st.sidebar:
        st.subheader("📚 Minhas Consultas")
        historico = carregar_historico_chat(email)
        chat_selecionado = None
        if isinstance(historico, list) and len(historico) > 0:
            for h in historico:
                if isinstance(h, dict) and 'pergunta' in h:
                    col_hist, col_del = st.columns([5, 1])
                    if col_hist.button(f"💬 {str(h['pergunta'])[:20]}...", key=f"hist_{h.get('id', 'x')}", use_container_width=True):
                        chat_selecionado = h
                    if col_del.button("🗑️", key=f"del_{h.get('id', 'x')}"):
                        mover_para_lixeira(h['id'])
                        st.rerun()
        
        st.divider()
        st.subheader("📎 Dissecador de Arquivos")
        st.write("Suba um PDF/DOCX do seu professor para cruzar com as diretrizes globais.")
        arquivo_upload = st.file_uploader("Enviar Material", type=["pdf", "docx", "txt"])

    st.markdown("### 🧠 Core AI | Terminal Clínico Avançado")
    pergunta = st.chat_input("Insira o tema ou dúvida médica...")
    
    dados_exibicao = None

    if pergunta:
        texto_extraido = ler_arquivo_texto(arquivo_upload) if arquivo_upload else ""
        with st.spinner("Analisando literatura e processando documento..."):
            resposta, area, subtema = consultar_core_ia_perfeicao(pergunta, texto_extraido)
            salvar_historico_chat(email, pergunta, resposta, area, subtema)
            dados_exibicao = {"q": pergunta, "a": resposta, "area": area, "subtema": subtema}
    elif chat_selecionado:
        dados_exibicao = {"q": chat_selecionado.get('pergunta', ''), "a": chat_selecionado.get('resposta', ''), "area": chat_selecionado.get('grande_area', ''), "subtema": chat_selecionado.get('subtema', '')}

    if dados_exibicao:
        with st.container(border=True):
            st.markdown(f"**Tema:** {dados_exibicao['q']}")
            st.markdown(dados_exibicao['a'])
            st.caption(f"🏷️ Classificação: **{dados_exibicao['area']} | {dados_exibicao['subtema']}**")
            
            st.divider()
            st.write("🛠️ **Exportação de Estudo (Salva no Banco Global):**")
            col1, col2, col3, col4 = st.columns(4)
            
            if col1.button("📥 Enviar p/ Resumos", icon="📘"):
                if salvar_item_estudo({"pergunta": f"Resumo Oficial: {dados_exibicao['q']}", "resposta": dados_exibicao['a'], "grande_area": dados_exibicao['area'], "subtema": dados_exibicao['subtema'], "categoria": "Resumo", "is_global": True, "criado_por_email": email}):
                    st.toast("✅ Salvo com sucesso no Master Study!")
                else: st.error("Erro ao salvar no banco.")
                
            if col2.button("🎴 Gerar Flashcards", icon="⚡"):
                with st.spinner("Minerando conhecimento..."):
                    qtd = gerar_apenas_flashcards(dados_exibicao['a'], dados_exibicao['area'], dados_exibicao['subtema'], email)
                    if qtd > 0: st.success(f"✅ {qtd} Cards salvos!")
                    else: st.error("Erro: JSON da IA corrompido.")
            
            if col3.button("📝 Criar Simulado", icon="🎯"):
                with st.spinner("Formulando questões ABCD..."):
                    qtd = gerar_apenas_questoes(dados_exibicao['a'], dados_exibicao['area'], dados_exibicao['subtema'], email)
                    if qtd > 0: st.success(f"✅ {qtd} Questões salvas!")
                    else: st.error("Erro: JSON da IA corrompido.")
            
            pdf_data = gerar_pdf_resposta(dados_exibicao['a'], email)
            col4.download_button("📄 Baixar PDF Lindo", data=pdf_data, file_name="Protocolo_NEXUS.pdf", mime="application/pdf")
