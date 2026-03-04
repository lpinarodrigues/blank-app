import streamlit as st
from database import listar_flashcards, listar_questoes, get_supabase, mover_para_lixeira, atualizar_progresso_sm2

def show():
    st.title("🎓 Master Study | Hub de Performance")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # Criando as 3 frentes de estudo em abas
    tab_resumos, tab_cards, tab_simulados = st.tabs([
        "📘 Protocolos & Resumos", 
        "🎴 Flashcards (Repetição Espaçada)", 
        "📝 Banco de Questões"
    ])

    # --- ABA 1: RESUMOS ---
    with tab_resumos:
        st.subheader("Meus Protocolos Salvos")
        try:
            res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            itens = [i for i in res.data if isinstance(i, dict)] if res.data else []
        except: itens = []

        if not itens:
            st.info("Nenhum resumo encontrado. Gere um no Core AI!")
        else:
            for item in itens:
                with st.container(border=True):
                    col_t, col_del = st.columns([10, 1])
                    col_t.markdown(f"### {item.get('pergunta', 'Sem Título')}")
                    if col_del.button("🗑️", key=f"del_res_{item['id']}"):
                        mover_para_lixeira(item['id'])
                        st.rerun()
                    
                    st.caption(f"🏷️ {item.get('grande_area', 'Geral')} | {item.get('subtema', 'Geral')}")
                    with st.expander("Expandir Conteúdo Completo"):
                        st.markdown(item.get('resposta', 'Sem conteúdo'))

    # --- ABA 2: FLASHCARDS ---
    with tab_cards:
        st.subheader("Revisão Ativa")
        all_cards = listar_flashcards(email)
        cards = [c for c in all_cards if c.get('categoria') == 'Flashcard']
        
        if not cards:
            st.info("Você ainda não tem flashcards para revisar.")
        else:
            for card in cards:
                with st.expander(f"🎴 {str(card.get('pergunta'))[:70]}..."):
                    st.markdown(f"**Pergunta:**\n{card.get('pergunta')}")
                    st.divider()
                    st.markdown(f"**Resposta:**\n{card.get('resposta')}")
                    
                    st.write("Qual foi o seu nível de facilidade?")
                    c1, c2, c3, c4 = st.columns([1,1,1,1])
                    if c1.button("🟢 Fácil", key=f"f_{card['id']}"): 
                        atualizar_progresso_sm2(card['id'], 5)
                        st.toast("Revisão agendada para daqui a 15 dias!")
                    if c2.button("🟡 Médio", key=f"m_{card['id']}"): 
                        atualizar_progresso_sm2(card['id'], 3)
                        st.toast("Revisão agendada para daqui a 3 dias!")
                    if c3.button("🔴 Difícil", key=f"d_{card['id']}"): 
                        atualizar_progresso_sm2(card['id'], 1)
                        st.toast("Revisão agendada para hoje!")
                    if c4.button("🗑️", key=f"del_card_{card['id']}"):
                        mover_para_lixeira(card['id'])
                        st.rerun()

    # --- ABA 3: QUESTÕES ---
    with tab_simulados:
        st.subheader("Treinamento de Questões")
        questoes = listar_questoes(email)
        
        if not questoes:
            st.info("Nenhuma questão no seu banco de dados.")
        else:
            for i, q in enumerate(questoes):
                with st.container(border=True):
                    st.markdown(f"**Questão {i+1}**")
                    st.write(q.get('pergunta'))
                    
                    opcoes = {
                        "A": q.get('opcao_a'),
                        "B": q.get('opcao_b'),
                        "C": q.get('opcao_c'),
                        "D": q.get('opcao_d')
                    }
                    
                    escolha = st.radio("Selecione a alternativa:", options=["A", "B", "C", "D"], key=f"q_radio_{q['id']}")
                    
                    if st.button("Verificar Gabarito", key=f"btn_q_{q['id']}"):
                        if escolha == q.get('gabarito'):
                            st.success(f"Correto! Alternativa {escolha}")
                        else:
                            st.error(f"Incorreto. O gabarito é {q.get('gabarito')}")
                        
                        st.info(f"**Justificativa:** {q.get('explica_correta')}")
