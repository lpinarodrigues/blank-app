import streamlit as st
import base64
from utils.ia_engine import consultar_core_ia_perfeicao, gerar_apenas_flashcards, gerar_apenas_questoes, ler_documento_universal, gerar_pdf_premium
from database import salvar_item_estudo

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    st.markdown("""
        <style>
        .stMetric { background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #334155; }
        .action-card { background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Terminal Oráculo Nexus | Visão & Síntese")

    # --- INPUTS DE ORGANIZAÇÃO ---
    c_org1, c_org2 = st.columns(2)
    area_med = c_org1.selectbox("📍 Grande Área", ["Clínica Médica", "Cirurgia", "Pediatria", "Ginecologia", "Preventiva"])
    subtema_med = c_org2.text_input("🏷️ Subtema/Doença", "Geral")

    # --- UPLOADS ---
    col_up1, col_up2 = st.columns(2)
    doc_up = col_up1.file_uploader("📂 PDF/Aula", type=["pdf", "docx", "pptx"])
    img_up = col_up2.file_uploader("📷 Imagem/Exame", type=["jpg", "png", "jpeg"])

    if doc_up:
        with st.container():
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.markdown(f"#### 📑 Processador Ativo: `{doc_up.name}`")
            c1, c2 = st.columns(2)
            q_cards = c1.slider("Cards", 5, 50, 15)
            q_qs = c2.slider("Questões", 1, 20, 5)
            
            if st.button("🔥 GERAR PROTOCOLO OURO & MATERIAL", use_container_width=True, type="primary"):
                st.session_state.auto_prompt = f"Analise este material de {area_med} sobre {subtema_med} e crie o Protocolo Ouro definitivo."
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # --- CHAT ENGINE ---
    if "messages" not in st.session_state: st.session_state.messages = []
    if "ultima_res" not in st.session_state: st.session_state.ultima_res = None

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    prompt = st.chat_input("Dúvida diagnóstica ou comando...")
    if st.session_state.get('auto_prompt'):
        prompt = st.session_state.auto_prompt
        del st.session_state['auto_prompt']

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("O Oráculo está a ler as evidências..."):
                txt_ctx = ler_documento_universal(doc_up)
                img_b64 = base64.b64encode(img_up.getvalue()).decode() if img_up else None
                res, a, s = consultar_core_ia_perfeicao(prompt, txt_ctx[:20000], img_b64)
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.session_state.ultima_res = {"q": prompt, "a": res, "area": area_med, "sub": subtema_med}

    if st.session_state.ultima_res:
        st.divider()
        d = st.session_state.ultima_res
        c1, c2, c3 = st.columns(3)
        if c1.button("💾 Salvar Protocolo", use_container_width=True):
            salvar_item_estudo({"pergunta": d['q'], "resposta": d['a'], "grande_area": d['area'], "subtema": d['sub'], "categoria": "Resumo", "criado_por_email": email})
            st.toast("Protocolo Arquivado!")
        if c2.button("🎴 Gerar Cards", use_container_width=True):
            gerar_apenas_flashcards(d['a'], d['area'], d['sub'], email, 10)
            st.toast("Flashcards Criados!")
        pdf = gerar_pdf_premium(d['a'], titulo=d['sub'])
        c3.download_button("📄 Exportar PDF", data=pdf, file_name=f"{d['sub']}.pdf", use_container_width=True)
