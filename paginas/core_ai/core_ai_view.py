import streamlit as st
from utils.ia_engine import consultar_core_ia_avancado

def show():
    st.markdown("### 🧠 Core AI | Oráculo de Diretrizes")
    st.caption("Consulta em tempo real via Groq (LPU) e Gemini 1.5 Pro.")

    # Container de Pesquisa
    with st.container(border=True):
        query = st.text_input("Sua dúvida clínica:", placeholder="Ex: Protocolo de Infarto com supra de ST...")
        
        if st.button("Consultar Diretrizes ⚡", use_container_width=True):
            if query:
                with st.status("Acionando Agentes de Elite...", expanded=True) as status:
                    st.write("📡 Conectando ao Groq para análise rápida...")
                    # Aqui chamamos a função real que usa as tuas chaves
                    resposta, check = consultar_core_ia_avancado(query)
                    
                    st.write("🛡️ Validando com Gemini (Core Checker)...")
                    status.update(label="Análise Concluída!", state="complete")
                
                # Exibição da Devolutiva Real
                st.markdown("#### 🛡️ Conduta Sugerida:")
                st.markdown(resposta)
                
                with st.expander("🔍 Verificação de Segurança (Checker)"):
                    st.info(check)
            else:
                st.warning("Por favor, digite uma dúvida para pesquisar.")

    st.divider()
    st.write("📚 **Fontes:** ESC, AHA, SBC, e Protocolos Unifesp/Dante.")
