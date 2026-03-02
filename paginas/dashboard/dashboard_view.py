import streamlit as st

def show():
    st.markdown("### 📊 Painel de Performance Médica")
    col1, col2, col3 = st.columns(3)
    col1.metric("Core Score", "850", "+12")
    col2.metric("Casos Revistos", "42", "7")
    col3.metric("Precisão IA", "98%", "1%")
    
    st.divider()
    st.subheader("📋 Próximas Revisões")
    st.info("• Diretriz de Insuficiência Cardíaca (SOCERJ)\n• Manejo de Infarto com Supra (Dante Pazzanese)")
