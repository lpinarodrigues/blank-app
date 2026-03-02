import streamlit as st
import pandas as pd
from shared_logic import salvar_log_auditoria, gerar_codificacao_seguranca

def show():
    st.title("📅 Planejamento Estratégico")
    st.markdown("### 🏛️ Gestão de Projetos e Atividades Acadêmicas")

    tabs = st.tabs(["🚀 Ciclo de Pesquisa", "🏥 Atividades Institucionais", "📋 Autogovernança"])

    with tabs[0]:
        st.subheader("Fases do Projeto de Pesquisa Principal")
        df_pesquisa = pd.DataFrame({
            "Etapa": ["Coleta", "Análise", "Escrita", "Submissão"],
            "Prazo": ["Mar/26", "Abr/26", "Mai/26", "Jun/26"],
            "Status": ["Em Curso", "Pendente", "Aguardando", "Planejado"]
        })
        st.table(df_pesquisa)
        
    with tabs[1]:
        st.subheader("Calendário Acadêmico / Extensão")
        st.info("Eventos, Aulas e Workshops planejados para o semestre.")

    with tabs[2]:
        st.subheader("Checklist de Atividades")
        if st.button("Registrar Conclusão de Ciclo"):
            h_id = gerar_codificacao_seguranca(st.session_state.user_email, "Cronograma_Update")
            salvar_log_auditoria(st.session_state.user_email, "Checklist_Geral", h_id)
            st.success(f"Log de auditoria gerado: {h_id}")
