import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from database import get_core_score, obter_ranking_elite

def gerar_radar_chart():
    # Categorias críticas para o Ciclo Clínico e Internato
    categories = ['Eletrocardiograma', 'Valvopatias', 'Farmacologia', 'Semiologia', 'Emergência', 'Conduta Clínica']
    
    # Valores simulados (que futuramente serão extraídos dos acertos no Supabase)
    values = [85, 60, 90, 75, 70, 80]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Competências',
        line_color='#1E3A8A'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#EEE")
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def show():
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    st.markdown("### 📊 Dashboard | CORE NEXUS")
    
    # 1. Grid de Métricas de Topo (Monday Style)
    col1, col2, col3 = st.columns(3)
    score = get_core_score(email)
    with col1:
        st.metric("Core Score", f"{score} pts", delta="+45")
    with col2:
        st.metric("Precisão Geral", "78%", delta="2%")
    with col3:
        st.metric("Nível", "Interno Pro", help="Status baseado no engajamento semanal")

    st.divider()
    
    # 2. Visualização de Dados Cruzada
    col_radar, col_activity = st.columns([1, 1])
    
    with col_radar:
        st.markdown("#### 🎯 Radar de Competências")
        st.caption("Foco: Ciclo Clínico e Internato")
        fig = gerar_radar_chart()
        st.plotly_chart(fig, use_container_width=True)
        
    with col_activity:
        st.markdown("#### 📈 Engajamento de Estudo")
        st.caption("Consistência de atividade semanal (Manhã/Tarde/Noite)")
        chart_data = pd.DataFrame(
            np.random.randint(5, 20, size=(7, 3)),
            columns=['Manhã', 'Tarde', 'Noite']
        )
        st.bar_chart(chart_data)

    st.divider()
    
    # 3. Ranking e Task List (Checklist de Pendências)
    col_rank, col_todo = st.columns([1.2, 0.8])
    
    with col_rank:
        st.markdown("#### 🏆 Ranking de Elite (SBC/TEC)")
        ranking = obter_ranking_elite()
        if ranking:
            df = pd.DataFrame(ranking).head(5)
            st.dataframe(
                df[['email', 'aproveitamento']].rename(columns={'email': 'Membro', 'aproveitamento': '% Acerto'}),
                hide_index=True, use_container_width=True
            )
        else:
            st.info("Aguardando simulados...")
            
    with col_todo:
        st.markdown("#### 📋 Pendências (Checklist)")
        st.checkbox("Revisar Conduta de IAM", value=False)
        st.checkbox("Validar Handoff Leito 402", value=True)
        st.checkbox("Fazer 10 flashcards", value=False)
