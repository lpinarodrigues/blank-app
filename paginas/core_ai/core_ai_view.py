import streamlit as st
import base64
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, gerar_pdf_resposta, ler_arquivo_texto
from database import salvar_item_estudo

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    st.markdown("### 🧠 Terminal Clínico Avançado | Oráculo Multimodal")
    
    st.markdown("<style>.st-emotion-cache-12w0qpk { background: #1e293b; border-radius: 12px; border-left: 5px solid #3b82f6; }</style>", unsafe_allow_html=True)

    col_up1, col_up2 = st.columns(2)
    with col_up1:
        with st.expander("📎 Documento Base (PDF/Texto)", expanded=False):
            doc_upload = st.file_uploader("", type=["pdf", "docx", "txt"], key="doc_up")
    with col_up2:
        with st.expander("🖼️ Análise de Imagem (ECG/Lab)", expanded=False):
            foto_exame = st.file_uploader("", type=["jpg", "png", "jpeg"], key="img_up")

    if "messages" not in st.session_state: st.session_state.messages = []
    if "ultima_resposta" not in st.session_state: st.session_state.ultima_resposta = None

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Dúvida médica ou conduta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sincronizando evidências..."):
                texto_contexto = ler_arquivo_texto(doc_upload) if doc_upload else ""
                img_b64 = base64.b64encode(foto_exame.getvalue()).decode() if foto_exame else None
                
                res, area, sub = consultar_core_ia_perfeicao(prompt, texto_contexto, img_b64)
                
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.session_state.ultima_resposta = {"q": prompt, "a": res, "area": area, "sub": sub}

    if st.session_state.ultima_resposta:
        st.divider()
        st.markdown("#### ⚙️ Gerador de Material de Estudo")
        d = st.session_state.ultima_resposta
        
        # SLIDERS DE QUANTIDADE
        c_qtd1, c_qtd2 = st.columns(2)
        qtd_cards = c_qtd1.slider("Quantidade de Flashcards", min_value=1, max_value=20, value=5)
        qtd_questoes = c_qtd2.slider("Quantidade de Questões", min_value=1, max_value=10, value=3)
        
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("📥 Salvar Resumo"): 
            salvar_item_estudo({"pergunta": d['q'], "resposta": d['a'], "grande_area": d['area'], "subtema": d['sub'], "categoria": "Resumo", "criado_por_email": email})
            st.toast("✅ Salvo na Biblioteca!")
        if c2.button(f"🎴 Gerar {qtd_cards} Cards"): 
            with st.spinner(f"Gerando {qtd_cards} flashcards..."):
                gerados = gerar_apenas_flashcards(d['a'], d['area'], d['sub'], email, qtd_cards)
                st.toast(f"✅ {gerados} Cards Gerados!")
        if c3.button(f"📝 Gerar {qtd_questoes} Questões"): 
            with st.spinner(f"Criando {qtd_questoes} questões..."):
                geradas = gerar_apenas_questoes(d['a'], d['area'], d['sub'], email, qtd_questoes)
                st.toast(f"✅ {geradas} Questões Criadas!")
        try:
            pdf = gerar_pdf_resposta(d['a'], email)
            c4.download_button("📄 PDF Premium", data=pdf, file_name="nexus_protocolo.pdf")
        except: c4.button("📄 PDF Indisponível", disabled=True)
