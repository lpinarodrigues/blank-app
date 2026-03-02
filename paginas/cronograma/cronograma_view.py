import streamlit as st

def show():
    st.title("📅 Gestão de Cronograma | CORE")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Projetos Ativos")
        with st.container(border=True):
            st.markdown("#### 📑 Linha de Pesquisa I (Acadêmico)")
            st.progress(75, text="Progresso: 75%")
            st.caption("Status: Fase de Discussão Técnica")
            
        with st.container(border=True):
            st.markdown("#### 🧬 Projeto Institucional II (Experimental)")
            st.progress(30, text="Progresso: 30%")
            st.caption("Status: Coleta de Dados Primários")

    with col2:
        st.subheader("✅ Metas Urgentes")
        st.checkbox("Validar bibliografia Vancouver")
        st.checkbox("Revisar Flashcards pendentes")
        st.button("🤖 IA: Planejar minha semana")
