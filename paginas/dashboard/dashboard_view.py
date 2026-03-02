import streamlit as st

def show():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>📊 Painel de Controle de Elite</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Desempenho Geral", value="85%", delta="5%")
    with col2:
        st.metric(label="Flashcards Revisados", value="128", delta="12")
    with col3:
        st.metric(label="Simulados Concluídos", value="14", delta="2")

    st.divider()
    
    opcoes = st.columns(2)
    with opcoes[0]:
        with st.expander("❤️ Cardiologia Clínica", expanded=True):
            st.write("- Valvopatias (Revisar em 2 dias)")
            st.write("- Insuficiência Cardíaca (Atualizado)")
    with opcoes[1]:
        with st.expander("⚡ Arritmias e ECG", expanded=True):
            st.write("- Fibrilação Atrial")
            st.write("- Taquicardias Supraventriculares")
