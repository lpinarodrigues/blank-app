import streamlit as st
import pandas as pd
import time
from database import listar_flashcards, atualizar_revisao_card, obter_estatisticas_estudo

def show():
    st.markdown("### 🧬 Master Study | Centro de Retenção")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    # --- LOGICA DE DADOS REAIS ---
    df_stats = obter_estatisticas_estudo(email)
    cards = listar_flashcards(email)
    
    # 1. NAVIGATION DE ALTO NÍVEL (Abas que funcionam)
    aba_praticar, aba_resumos, aba_questoes = st.tabs(["🔥 Praticar (Flashcards)", "📚 Caderno de Resumos", "📝 Gerador de Provas"])

    with aba_praticar:
        if not cards:
            st.info("Seu deck está vazio. Vá ao 'Core AI' ou suba um arquivo em 'Simulados' para gerar conhecimento.")
        else:
            # Filtro de Repetição Espaçada (Algoritmo SM-2)
            hoje = pd.Timestamp.now().date()
            cards_hoje = [c for c in cards if pd.to_datetime(c.get('proxima_revisao', '2000-01-01')).date() <= hoje]
            
            st.write(f"**Revisões para hoje:** {len(cards_hoje)} cards")
            
            if cards_hoje:
                card = cards_hoje[0]
                with st.container(border=True):
                    st.caption(f"Área: {card.get('grande_area', 'Geral')} | Subtema: {card.get('subtema', 'Geral')}")
                    st.markdown(f"### {card['pergunta']}")
                    
                    if st.button("👁️ Revelar Resposta", use_container_width=True):
                        st.markdown(f"**Resposta:** {card['resposta']}")
                        if card.get('explicacao'):
                            st.info(f"💡 Justificativa: {card['explicacao']}")
                        
                        st.divider()
                        st.write("Qual foi o nível de dificuldade?")
                        cols = st.columns(4)
                        btn_labels = [("❌ Esqueci", 1), ("⚠️ Difícil", 3), ("✅ Bom", 4), ("⚡ Fácil", 5)]
                        for i, (label, val) in enumerate(btn_labels):
                            if cols[i].button(label):
                                atualizar_revisao_card(card['id'], val)
                                st.rerun()
            else:
                st.success("🎉 Você completou suas revisões diárias!")

    with aba_resumos:
        st.subheader("📖 Seus Resumos Estruturados")
        if not df_stats.empty:
            areas = df_stats['grande_area'].unique()
            selecao = st.selectbox("Filtrar por Área:", areas)
            
            resumos_area = df_stats[df_stats['grande_area'] == selecao]
            for _, row in resumos_area.iterrows():
                with st.expander(f"📍 {row['subtema']} - Revisões: {row['revisões_totais']}"):
                    st.write(f"**Facilidade do Tema:** {row['facilidade']}/5.0")
                    st.progress(min(row['facilidade']/5.0, 1.0))
        else:
            st.warning("Nenhum resumo gerado ainda. Use a IA para converter casos clínicos em resumos.")

    with aba_questoes:
        st.subheader("📝 Simulado Personalizado")
        col1, col2 = st.columns(2)
        area_sim = col1.selectbox("Eixo Principal:", ["Clínica Médica", "Cirurgia", "Pediatria", "Preventiva"])
        qtd = col2.slider("Quantidade de Questões:", 5, 50, 10)
        
        if st.button("Iniciar Simulado de Elite 🚀"):
            st.session_state.modo_simulado = True
            st.write(f"Gerando {qtd} questões de {area_sim} com base no seu histórico de erros...")
            # Lógica de geração dinâmica aqui
