import streamlit as st
import pandas as pd
from database import listar_flashcards, listar_biblioteca_global, adotar_item_global, atualizar_progresso_sm2

def show_flashcards(email):
    st.subheader("🎴 Ecossistema de Flashcards")
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🔥 Praticar", "👤 Minha Biblioteca", "🌎 Biblioteca Global"])
    
    with sub_tab3:
        st.caption("Cards compartilhados pela elite CORE NEXUS")
        global_cards = listar_biblioteca_global(limit=50)
        if global_cards:
            df_g = pd.DataFrame(global_cards)[['grande_area', 'subtema', 'pergunta', 'id']]
            st.dataframe(df_g, use_container_width=True)
            sel_id = st.selectbox("Selecione um ID para adotar no seu deck:", df_g['id'])
            if st.button("📥 Adicionar à Minha Biblioteca"):
                adotar_item_global(sel_id, email)
                st.success("Card clonado com sucesso!")
        else: st.info("Nenhum card global disponível ainda.")

    with sub_tab1:
        # Aqui entra o motor de repetição já codificado anteriormente
        st.info("Iniciando motor de Repetição Espaçada...")

def show_questoes(email):
    st.subheader("📝 Ecossistema de Questões")
    q_tab1, q_tab2 = st.tabs(["✍️ Fazer Simulado", "📚 Banco de Questões Global"])
    with q_tab2:
        st.write("Banco de Dados Verídico (Clínica/Cirurgia)")
        # Filtros por Área/Subtema aqui

def show_resumos(email):
    st.subheader("📖 Ecossistema de Resumos")
    r_tab1, r_tab2 = st.tabs(["📓 Meus Cadernos", "🌐 Repositório Unifesp/Dante"])

def show():
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    # TRIFURCAÇÃO PRINCIPAL
    modulo = st.sidebar.selectbox("Escolha o Módulo Master:", ["🎴 Flashcards", "📝 Questões", "📖 Resumos"])
    
    if modulo == "🎴 Flashcards":
        show_flashcards(email)
    elif modulo == "📝 Questões":
        show_questoes(email)
    elif modulo == "📖 Resumos":
        show_resumos(email)
