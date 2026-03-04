import streamlit as st
import base64
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, ler_documento_universal, gerar_pdf_premium
from database import salvar_item_estudo

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # --- CSS PREMIUM GLASSMORPHISM ---
    st.markdown("""
        <style>
        .core-header {
            background: linear-gradient(90deg, #1e293b, #0f172a);
            padding: 20px; border-radius: 16px; border-bottom: 3px solid #3b82f6;
            margin-bottom: 25px; text-align: center; color: white;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .upload-box {
            background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px);
            border: 1px dashed #475569; border-radius: 12px; padding: 10px;
        }
        .auto-action-panel {
            background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;
            border-radius: 12px; padding: 20px; margin-top: 15px; margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='core-header'><h2>🧠 Terminal Oráculo Nexus</h2><p>Análise Diagnóstica, Síntese de Aulas e Geração de Protocolos</p></div>", unsafe_allow_html=True)

    # --- ZONA DE UPLOAD UNIVERSAL ---
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        doc_upload = st.file_uploader("📚 Enviar Aula/Artigo (PDF, PPTX, DOCX)", type=["pdf", "docx", "pptx", "txt"], key="doc_up")
    with col_up2:
        foto_exame = st.file_uploader("🖼️ Enviar Exame/ECG (JPG, PNG)", type=["jpg", "png", "jpeg"], key="img_up")
    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # NOVO: LABORATÓRIO AUTOMÁTICO DO DOCUMENTO (Gatilho Imediato)
    # =========================================================================
    if doc_upload:
        st.markdown("<div class='auto-action-panel'>", unsafe_allow_html=True)
        st.markdown(f"### ⚡ Processador de Ficheiro: `{doc_upload.name}`")
        st.caption("Escolha o que deseja extrair deste documento. A IA fará a leitura silenciosa e enviará direto para o Master Study.")
        
        # Sliders EXCLUSIVOS para o documento
        c_qtd1, c_qtd2 = st.columns(2)
        qtd_cards_doc = c_qtd1.slider("🎴 Flashcards a gerar", min_value=1, max_value=30, value=10, key="sld_doc_card")
        qtd_questoes_doc = c_qtd2.slider("📝 Questões a gerar", min_value=1, max_value=15, value=5, key="sld_doc_qst")
        
        b1, b2, b3 = st.columns(3)
        
        # Botão 1: Resumo Inteligente (Joga para o Chat)
        if b1.button("📑 Gerar Resumo Estruturado", use_container_width=True, type="primary"):
            st.session_state.auto_prompt = f"Por favor, atue como um professor de medicina e faça um resumo clínico, estruturado em tópicos e focado nos pontos principais para prova de residência baseando-se no ficheiro: {doc_upload.name}"
            st.rerun() # Reinicia a página para jogar o prompt no chat automaticamente
            
        # Botão 2: Gerar Flashcards Direto do Ficheiro
        if b2.button(f"⚡ Extrair {qtd_cards_doc} Cards", use_container_width=True):
            with st.spinner("A ler o documento e a extrair cards de alta retenção..."):
                texto_puro = ler_documento_universal(doc_upload)[:15000] # Limite de segurança para não explodir a memória
                gerados = gerar_apenas_flashcards(texto_puro, "Clínica", "Doc_Automático", email, qtd_cards_doc)
                if gerados > 0:
                    st.success(f"✅ {gerados} Cards Gerados e enviados para Revisão!")
                else:
                    st.error("Erro ao gerar cards. Verifique o conteúdo do ficheiro.")
                
        # Botão 3: Gerar Simulados Direto do Ficheiro
        if b3.button(f"🎯 Criar {qtd_questoes_doc} Questões", use_container_width=True):
            with st.spinner("A ler o documento e a criar simulado padrão residência..."):
                texto_puro = ler_documento_universal(doc_upload)[:15000]
                geradas = gerar_apenas_questoes(texto_puro, "Clínica", "Doc_Automático", email, qtd_questoes_doc)
                if geradas > 0:
                    st.success(f"✅ {geradas} Questões Criadas e enviadas para o Simulado!")
                else:
                    st.error("Erro ao criar questões. Tente novamente.")
                
        st.markdown("</div>", unsafe_allow_html=True)
    # =========================================================================

    # --- CHATBOT ---
    if "messages" not in st.session_state: st.session_state.messages = []
    if "ultima_resposta" not in st.session_state: st.session_state.ultima_resposta = None
    if "auto_prompt" not in st.session_state: st.session_state.auto_prompt = None # Variável fantasma para gatilhos

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # Define se a entrada vem do utilizador a digitar OU do botão de "Gerar Resumo"
    prompt_usuario = st.chat_input("Dúvida médica, caso clínico ou comando...")
    if st.session_state.auto_prompt:
        prompt_usuario = st.session_state.auto_prompt
        st.session_state.auto_prompt = None # Limpa após usar

    if prompt_usuario:
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"): st.markdown(prompt_usuario)

        with st.chat_message("assistant"):
            with st.spinner("A sincronizar banco de dados médico..."):
                texto_contexto = ler_documento_universal(doc_upload) if doc_upload else ""
                if texto_contexto: texto_contexto = texto_contexto[:15000] # Segurança
                img_b64 = base64.b64encode(foto_exame.getvalue()).decode() if foto_exame else None
                
                res, area, sub = consultar_core_ia_perfeicao(prompt_usuario, texto_contexto, img_b64)
                
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.session_state.ultima_resposta = {"q": prompt_usuario, "a": res, "area": area, "sub": sub}

    # --- PAINEL DE CONTROLO DE ESTUDO (A PARTIR DA CONVERSA) ---
    if st.session_state.ultima_resposta:
        st.divider()
        st.markdown("### ⚙️ Sintetizador da Conversa Atual")
        d = st.session_state.ultima_resposta
        
        c_qtd1, c_qtd2 = st.columns(2)
        qtd_cards_chat = c_qtd1.slider("🎴 Flashcards baseados na resposta", 1, 20, 5, key="sld_chat_card")
        qtd_questoes_chat = c_qtd2.slider("📝 Questões baseadas na resposta", 1, 10, 3, key="sld_chat_qst")
        
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("📥 Salvar Protocolo", use_container_width=True): 
            salvar_item_estudo({"pergunta": d['q'], "resposta": d['a'], "grande_area": d['area'], "subtema": d['sub'], "categoria": "Resumo", "criado_por_email": email})
            st.toast("✅ Salvo no Master Study!")
            
        if c2.button(f"⚡ Criar {qtd_cards_chat} Cards", use_container_width=True): 
            with st.spinner("A extrair conceitos..."):
                gerados = gerar_apenas_flashcards(d['a'], d['area'], d['sub'], email, qtd_cards_chat)
                st.toast(f"✅ {gerados} Cards Gerados!")
                
        if c3.button(f"🎯 Criar {qtd_questoes_chat} Questões", use_container_width=True): 
            with st.spinner("A formular simulado..."):
                geradas = gerar_apenas_questoes(d['a'], d['area'], d['sub'], email, qtd_questoes_chat)
                st.toast(f"✅ {geradas} Questões Criadas!")
                
        try:
            pdf_bytes = gerar_pdf_premium(d['a'], titulo=d['q'][:50])
            c4.download_button("📄 Exportar PDF", data=pdf_bytes, file_name="Nexus_Protocolo.pdf", mime="application/pdf", use_container_width=True)
        except Exception as e:
            c4.button("📄 Erro no PDF", disabled=True, help=str(e))
