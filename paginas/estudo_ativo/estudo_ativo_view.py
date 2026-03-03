import streamlit as st
import google.generativeai as genai
from database import salvar_flashcard, listar_flashcards, update_score, atualizar_revisao_card
import pandas as pd

def show():
    st.markdown("### 📚 Master Study | Inteligência de Retenção")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    # 1. Dashboard de Retenção (Inspirado no Brainscape)
    cards = listar_flashcards(email)
    cards_hoje = [c for c in cards if pd.to_datetime(c.get('proxima_revisao', '2000-01-01')).date() <= pd.Timestamp.now().date()]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Cards", len(cards))
    col2.metric("Para Revisar", len(cards_hoje), delta_color="inverse")
    col3.metric("Domínio Médio", "72%")

    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🔥 Revisão Inteligente", "🧠 Gerador de Questões", "📊 Deck Completo"])

    with tab1:
        if not cards_hoje:
            st.success("🎉 Deck limpo! Você está em dia com suas sinapses.")
            st.balloons()
        else:
            card = cards_hoje[0] # Pega o primeiro da fila
            st.markdown(f"**CATEGORIA:** `{card.get('categoria', 'Geral')}`")
            
            with st.container(border=True):
                st.markdown(f"### {card['pergunta']}")
                
                if st.button("👁️ Revelar Resposta"):
                    st.markdown(f"--- \n **RESPOSTA:** \n {card['resposta']}")
                    
                    st.markdown("Como foi sua lembrança?")
                    cols = st.columns(4)
                    botoes = [("❌ Errei", 1, "red"), ("⚠️ Difícil", 3, "orange"), ("✅ Bom", 4, "blue"), ("⚡ Fácil", 5, "green")]
                    
                    for i, (label, qual, color) in enumerate(botoes):
                        if cols[i].button(label, key=f"btn_{qual}"):
                            atualizar_revisao_card(card['id'], qual)
                            update_score(email, qual * 2)
                            st.rerun()

    with tab2:
        st.subheader("Gerador de Questões Padrão TEC/SBC")
        tema = st.text_input("Tema para novos cards:", placeholder="Ex: Valvopatias Mitrais...")
        if st.button("Gerar 10 Cards de Elite ⚡"):
            with st.spinner("IA simulando banca examinadora..."):
                genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Gere 5 flashcards de alto nível sobre {tema} para residentes. Formato P: pergunta | R: resposta curta."
                res = model.generate_content(prompt).text
                for linha in res.split('\n'):
                    if '|' in linha:
                        p, r = linha.split('|')
                        salvar_flashcard(p.replace('P:','').strip(), r.replace('R:','').strip(), tema, email)
                st.success("Cards integrados ao seu algoritmo de repetição!")

    with tab3:
        if cards:
            df_cards = pd.DataFrame(cards)[['pergunta', 'categoria', 'intervalo', 'revisões_totais']]
            st.dataframe(df_cards, use_container_width=True, hide_index=True)
