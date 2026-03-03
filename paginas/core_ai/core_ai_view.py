import streamlit as st
from utils.ia_engine import consultar_core_ia_perfeicao

def show():
    st.markdown("### 🧠 Core AI | Oráculo de Elite")
    st.caption("DNA: UpToDate + Amboss + Diretrizes Dante/Unifesp")

    # Configurações de Resposta
    with st.sidebar:
        st.markdown("---")
        modo = st.radio("Foco da Resposta:", ["Beira de Leito", "Acadêmico"], index=0)
        st.info("O modo 'Beira de Leito' prioriza doses e ações imediatas.")

    # Container de Pesquisa
    with st.container(border=True):
        query = st.text_input("Qual a dúvida clínica de hoje?", placeholder="Ex: Manejo da Crise Hipertensiva na Gestação...")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            btn_consulta = st.button("Consultar Oráculo ⚡", use_container_width=True)
        with col2:
            # Botão inspirado no NeuralConsult para busca rápida de doses
            btn_dose = st.button("💊 Apenas Doses Rápidas", use_container_width=True)

        if btn_consulta or btn_dose:
            if query:
                final_query = query if btn_consulta else f"Qual a posologia e via de administração de: {query}"
                with st.status("Consultando base de evidências...", expanded=True) as status:
                    resposta, status_text = consultar_core_ia_perfeicao(final_query, modo)
                    status.update(label="Análise Concluída!", state="complete")
                
                # Exibição Padrão Ouro
                st.markdown("#### 🛡️ Conduta Sugerida:")
                st.markdown(resposta)
                
                st.divider()
                st.caption(f"🔍 {status_text}")
                
                # Ação Inspirada no Medsimple: Transformar em Flashcard
                if st.button("📥 Salvar como Flashcard de Revisão"):
                    st.toast("Conduta enviada para o Master Study!", icon="📚")
            else:
                st.warning("Por favor, insira uma dúvida para prosseguir.")

    st.divider()
    # Badge de Qualidade
    st.markdown('<div style="text-align: center; color: gray; font-size: 0.8em;">Baseado em Protocolos Institucionais e Diretrizes 2024-2026</div>', unsafe_allow_html=True)
