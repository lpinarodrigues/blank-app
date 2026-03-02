import streamlit as st
from datetime import datetime

def show():
    st.title("🔬 Sci-Core | Unidade de Pesquisa")
    st.markdown("---")

    menu = st.sidebar.radio("Navegação Científica:", 
                           ["🛠️ Oficina de Projetos", "📚 Acervo", "🔍 Análise Crítica", "🧠 Estudo Ativo"])

    if menu == "🛠️ Oficina de Projetos":
        st.header("🛠️ Oficina de Projetos")
        
        tab_gestao, tab_cronograma, tab_stats = st.tabs([
            "📋 Gestão Metodológica", "📅 Cronograma de Elite", "📊 Bioestatística"
        ])

        with tab_gestao:
            st.subheader("Framework de Pesquisa")
            st.selectbox("Desenho do Estudo:", ["Relato de Caso (CARE)", "Revisão Sistemática (PRISMA)", "STROBE", "CONSORT"])
            st.checkbox("Aprovação Ética (CEP/CONEP)")

        with tab_cronograma:
            st.subheader("📅 Master Timeline: FAPESP / Dante / UNIFESP")
            
            # --- DASHBOARD DE PROGRESSO ---
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown("### 📑 Projeto Principal (Dante)")
                    st.progress(75, text="75% - Fase de Escrita")
                    st.caption("🚨 **Deadline Submissão:** 30/04/2026")
                    if st.button("Ver Detalhes do Projeto A"):
                        st.info("Falta: Revisão das referências Vancouver e tabelas de resultados.")

            with col2:
                with st.container(border=True):
                    st.markdown("### 🧬 Linha de Pesquisa (UNIFESP)")
                    st.progress(30, text="30% - Coleta de Dados")
                    st.caption("📅 **Relatório Parcial FAPESP:** 15/06/2026")
                    if st.button("Ver Detalhes do Projeto B"):
                        st.warning("Atenção: Necessário N de 150 pacientes (Atuais: 45).")

            st.divider()
            
            # --- TO-DO LIST DE ALTO IMPACTO ---
            st.subheader("✅ To-Do List Científica")
            col_todo1, col_todo2 = st.columns([2, 1])
            
            nova_tarefa = col_todo1.text_input("", placeholder="Adicionar nova meta de pesquisa...")
            if col_todo2.button("Adicionar Meta", use_container_width=True):
                st.toast(f"Meta '{nova_tarefa}' adicionada!")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Burocrático / Ética**")
                st.checkbox("Submeter emenda na Plataforma Brasil")
                st.checkbox("Responder pendências do CEP")
                st.checkbox("Validar TCLEs assinados")
            with c2:
                st.markdown("**Execução / Escrita**")
                st.checkbox("Rodar multivariada no R/Python", value=True)
                st.checkbox("Finalizar Discussão (Comparativo ESC 2024)")
                st.checkbox("Gerar figuras em Alta Resolução")

        with tab_stats:
            st.subheader("📊 Bioestatística Aplicada")
            st.write("Calculadora 2x2 e interpretação de p-valor.")

    elif menu == "📚 Acervo":
        st.header("📚 Acervo")
    elif menu == "🔍 Análise Crítica":
        st.header("🔍 Análise Crítica")
    elif menu == "🧠 Estudo Ativo":
        st.header("🧠 Estudo Ativo")
