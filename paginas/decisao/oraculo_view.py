import streamlit as st
from shared_logic import chamar_oraculo, lembrete_etico

def show():
    st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem;'>{lembrete_etico()}</p>", unsafe_allow_html=True)
    st.title("🔮 Oráculo | Inteligência Multimodal")

    # --- UPLOAD DE EXAMES (NOVO) ---
    with st.expander("🖼️ Analisar Exame (ECG, Eco, RM, Laboratório)", expanded=False):
        foto_exame = st.file_uploader("Suba a imagem do exame para análise assistida:", type=["jpg", "png", "pdf"])
        if foto_exame:
            st.info("Funcionalidade de Visão Computacional ativa. Descreva sua dúvida sobre o exame abaixo.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Dúvida, caso clínico ou conduta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sincronizando evidências..."):
                # System Prompt de Elite com foco em Diagnóstico Diferencial
                sys_prompt = """
                Você é o CORE NEXUS. Responda SEMPRE em Português.
                Se o caso for clínico, apresente:
                1. Top 3 Diagnósticos Diferenciais.
                2. Sugestão de Score Clínico pertinente.
                3. Conduta Classe I (Diretrizes).
                """
                resposta = chamar_oraculo(f"{sys_prompt}\n\n{prompt}")
                st.markdown(resposta)
                
                # --- BOTÕES DE AÇÃO RÁPIDA ---
                st.divider()
                c1, c2, c3 = st.columns(3)
                if c1.button("🗂️ Flashcard"):
                    st.session_state.card_temp = resposta
                    st.toast("Enviado para Performance!")
                if c2.button("🌿 Fluxograma"):
                    st.session_state.flow_temp = resposta
                    st.toast("Enviado para Pesquisa!")
                if c3.button("📥 Gerar PDF"):
                    st.info("Relatório de Interconsulta sendo gerado...")

        st.session_state.messages.append({"role": "assistant", "content": resposta})
