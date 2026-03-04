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

    st.markdown("### 🧠 Core AI | Terminal Clínico Avançado")
    
    # UPLOADER NO CENTRO DA TELA
    with st.expander("📎 Anexar Documento Base (Opcional - PDF/DOCX)", expanded=False):
        st.write("Suba uma aula ou artigo para a IA cruzar com as diretrizes.")
        arquivo_upload = st.file_uploader("", type=["pdf", "docx", "txt"])

    pergunta = st.chat_input("Insira o tema, dúvida ou instrução sobre o arquivo anexado...")
    dados_exibicao = None

    if pergunta:
        texto_extraido = ler_arquivo_texto(arquivo_upload) if arquivo_upload else ""
        with st.spinner("Processando literatura e estruturando protocolo..."):
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
            st.write("🛠️ **Ações (Salvas no Master Study):**")
            col1, col2, col3, col4 = st.columns(4)
            
            if col1.button("📥 Enviar p/ Resumos", icon="📘"):
                salvar_item_estudo({"pergunta": f"Resumo Oficial: {dados_exibicao['q']}", "resposta": dados_exibicao['a'], "grande_area": dados_exibicao['area'], "subtema": dados_exibicao['subtema'], "categoria": "Resumo", "is_global": True, "criado_por_email": email})
                st.toast("✅ Salvo no Master Study!")
                
            if col2.button("🎴 Gerar Flashcards", icon="⚡"):
                with st.spinner("Minerando..."):
                    qtd = gerar_apenas_flashcards(dados_exibicao['a'], dados_exibicao['area'], dados_exibicao['subtema'], email)
                    if qtd > 0: st.success(f"✅ {qtd} Cards salvos!")
                    else: st.error("Erro na extração.")
            
            if col3.button("📝 Criar Simulado", icon="🎯"):
                with st.spinner("Criando ABCD..."):
                    qtd = gerar_apenas_questoes(dados_exibicao['a'], dados_exibicao['area'], dados_exibicao['subtema'], email)
                    if qtd > 0: st.success(f"✅ {qtd} Questões salvas!")
                    else: st.error("Erro na extração.")
            
            pdf_data = gerar_pdf_resposta(dados_exibicao['a'], email)
            col4.download_button("📄 Baixar PDF Lindo", data=pdf_data, file_name="Protocolo_NEXUS.pdf", mime="application/pdf")
