import streamlit as st
import pandas as pd
from database import get_core_score, obter_ranking_elite

def show():
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    st.markdown(f"### 📊 Dashboard de Performance")
    
    # Métricas de Topo
    score = get_core_score(email)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seu Core Score", f"{score} pts", delta="+15 hoje")
    with col2:
        st.metric("Status Global", "Elite" if score > 1000 else "Residente")

    st.divider()
    
    # --- RANKING DE ELITE ---
    st.markdown("#### 🏆 Ranking de Elite (SBC/TEC)")
    ranking = obter_ranking_elite()
    
    if ranking:
        df_ranking = pd.DataFrame(ranking).head(5)
        # Estilização de Tabela para Mobile
        st.table(df_ranking[['email', 'aproveitamento', 'total']].rename(columns={
            'email': 'Membro', 'aproveitamento': '% Acerto', 'total': 'Questões'
        }))
    else:
        st.info("Aguardando os primeiros simulados para gerar o ranking.")

    st.divider()
    
    # --- ÁREAS DE FOCO ---
    st.markdown("#### 🎯 Foco de Estudo Sugerido")
    st.caption("Baseado nos erros mais comuns da semana:")
    st.progress(0.3, text="Valvopatias (30% de acerto)")
    st.progress(0.8, text="Arritmias (80% de acerto)")
