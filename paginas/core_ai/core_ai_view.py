import streamlit as st
from utils.ia_engine import consultar_core_ia_avancado

def show():
    st.markdown("### 🧠 Core AI | Motor Híbrido Triplo")
    
    with st.container(border=True):
        query = st.text_area("Caso Clínico:", placeholder="Descreva o quadro...", height=100)
        
        if st.button("Executar Análise de Elite ⚡", use_container_width=True):
            with st.status("Acionando Agentes...", expanded=True) as status:
                st.write("🏃 Groq gerando base...")
                st.write("🧠 Gemini Pro refinando...")
                resposta, check = consultar_core_ia_avancado(query)
                st.write("🛡️ Gemini Flash validando segurança...")
                status.update(label="Análise Concluída com Tripla Checagem!", state="complete")
            
            st.markdown(f"**Conduta Sugerida:**\n\n{resposta}")
            
            with st.expander("🔍 Relatório do Core Checker"):
                st.info(check)
