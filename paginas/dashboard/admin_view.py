import streamlit as st
import plotly.express as px
from database import obter_metricas_admin

def show():
    if st.session_state.get('user_email') != "lucas.pina@unifesp.br":
        st.error("Acesso restrito ao Administrador Master.")
        return

    st.title("🛡️ Painel de Controle de Internato")
    
    t_cards, t_membros, df_erros = obter_metricas_admin()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Itens no Big Data", t_cards)
    col2.metric("Alunos Ativos", t_membros)
    col3.metric("Taxa de Engajamento", "88%")

    st.divider()
    st.subheader("🎯 Onde a turma está falhando?")
    if not df_erros.empty:
        fig = px.histogram(df_erros, x="grande_area", title="Volume de Erros por Área", color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig, use_container_width=True)
        st.info("Sugestão: Reforce 'Cirurgia Geral' na próxima reunião clínica.")
    else:
        st.success("Ainda não há dados de erros significativos.")
