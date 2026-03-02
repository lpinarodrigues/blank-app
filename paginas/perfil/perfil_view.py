import streamlit as st
from database import get_core_score
from utils.pdf_generator import gerar_relatorio_pdf

def show():
    st.markdown("### 👤 Gestão de Perfil e Relatórios")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    score = get_core_score(email)
    
    with st.container(border=True):
        st.write(f"**E-mail:** {email}")
        st.write(f"**Core Score Atual:** {score} pts")
        st.write("**Status:** Ativo no Sistema de Elite")
    
    st.divider()
    st.subheader("📄 Exportar Documentos")
    st.write("Gere um comprovante oficial do seu progresso de estudo ativo.")
    
    # Gerar o PDF no clique
    pdf_data = gerar_relatorio_pdf(email, score)
    
    st.download_button(
        label="📥 Baixar Relatório de Performance (PDF)",
        data=pdf_data,
        file_name=f"Relatorio_CoreNexus_{email}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
