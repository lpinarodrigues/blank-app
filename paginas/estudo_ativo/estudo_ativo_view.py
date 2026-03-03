import streamlit as st
import pandas as pd
from database import filtrar_banco_elite, atualizar_progresso_sm2, obter_estatisticas_estudo
from utils.ia_engine import dissecar_arquivo_master

def show():
    st.markdown("### 🧬 Master Study | Padrão Ouro Internacional")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    # 1. NAVEGAÇÃO REAL
    aba_revisao, aba_simulado, aba_upload = st.tabs(["🔥 Revisão Ativa", "📝 Simulados por Tema", "📤 Dissecador de PDFs"])

    with aba_revisao:
        st.subheader("Flashcards com Repetição Espaçada")
        cards = filtrar_banco_elite()
        if not cards:
            st.info("Nenhum card disponível. Use o Dissecador ou o Core AI para povoar seu banco.")
        else:
            card = cards[0] # Lógica de fila
            with st.container(border=True):
                st.caption(f"{card['grande_area']} > {card['subtema']}")
                st.markdown(f"### {card['pergunta']}")
                
                if st.button("👁️ Revelar Resposta"):
                    st.markdown(f"**Gabarito:** {card['resposta']}")
                    st.info(f"💡 Justificativa: {card.get('explicacao', 'Sem detalhes.')}")
                    
                    st.divider()
                    cols = st.columns(4)
                    labels = [("❌ Esqueci", 1), ("⚠️ Difícil", 3), ("✅ Bom", 4), ("⚡ Fácil", 5)]
                    for i, (l, v) in enumerate(labels):
                        if cols[i].button(l):
                            atualizar_progresso_sm2(card['id'], v)
                            st.rerun()

    with aba_simulado:
        st.subheader("Gerador de Provas por Área")
        col1, col2 = st.columns(2)
        area = col1.selectbox("Grande Área:", ["Todas", "Clínica Médica", "Cirurgia Geral", "Pediatria", "GO", "Preventiva"])
        sub = col2.selectbox("Subtema:", ["Todos", "Cardiologia", "Gastro", "Trauma", "Pneumologia"])
        
        if st.button("Iniciar Simulado do Banco 🚀"):
            questoes = filtrar_banco_elite(area, sub)
            if questoes:
                st.success(f"Encontradas {len(questoes)} questões no banco de Big Data.")
                for q in questoes[:5]:
                    with st.container(border=True):
                        st.write(q['pergunta'])
                        st.radio("Alternativas:", ["A", "B", "C", "D"], key=f"q_{q['id']}")
            else:
                st.warning("Sem questões para este filtro específico.")

    with aba_upload:
        st.subheader("Transformar PDF em Simulado de Elite")
        arquivo = st.file_uploader("Suba sua Diretriz ou Capítulo (PDF):", type=['pdf', 'txt'])
        if arquivo:
            area_up = st.selectbox("Área deste arquivo:", ["Cirurgia Geral", "Clínica Médica"])
            sub_up = st.text_input("Subtema (ex: Valvopatias):")
            
            if st.button("Dissecar e Gerar Prova ⚡"):
                with st.spinner("IA transformando PDF em questões padrão TEC..."):
                    conteudo = arquivo.read().decode("utf-8", errors="ignore")
                    questoes = dissecar_arquivo_master(conteudo, area_up, sub_up)
                    if questoes:
                        st.session_state.questoes_pdf = questoes
                        st.success("Simulado gerado com sucesso!")
        
        if 'questoes_pdf' in st.session_state:
            for i, q in enumerate(st.session_state.questoes_pdf):
                with st.expander(f"Questão {i+1}: {q['pergunta'][:50]}..."):
                    st.markdown(f"**{q['pergunta']}**")
                    ans = st.radio(f"Sua resposta (Q{i}):", ["A", "B", "C", "D"], key=f"ans_{i}")
                    if st.button(f"Validar Q{i}"):
                        if ans == q['gabarito']:
                            st.success(f"✅ Correto! {q['explica_correta']}")
                        else:
                            st.error(f"❌ Errado. O correto é {q['gabarito']}.")
                            st.markdown(f"**Por que você errou a {ans}:** {q['explica_erros'].get(ans)}")
                            st.warning(f"📚 **Reforce:** {q['reforco']}")
