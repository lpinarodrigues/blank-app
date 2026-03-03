import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import sys
import os

# Garante que a raiz do projeto está no path para achar o database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from database import get_core_score, obter_ranking_elite

def gerar_radar_chart():
    categories = ['Eletro', 'Valvas', 'Farmaco', 'Semio', 'Emerg', 'Conduta']
    values = [85, 60, 90, 75, 70, 80]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', line_color='#1E3A8A'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=300)
    return fig

def show():
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    st.title("📊 Dashboard")
    
    score = get_core_score(email)
    st.metric("Core Score", f"{score} pts")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Competências")
        st.plotly_chart(gerar_radar_chart(), use_container_width=True)
    with col_b:
        st.markdown("### Atividade")
        st.bar_chart(np.random.randn(7, 3))
    
    st.markdown("### Ranking")
    ranking = obter_ranking_elite()
    if ranking:
        st.table(pd.DataFrame(ranking).head(5))
