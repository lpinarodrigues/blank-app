import streamlit as st
from database import get_supabase, listar_flashcards, listar_questoes, mover_para_lixeira, atualizar_progresso_sm2

def show():
    st.title("🎓 Master Study | Hub de Performance")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # Criando as 3 abas principais
    tab_resumos, tab_cards, tab_questoes = st.tabs([
        "📘 Protocolos & Resumos", 
        "🎴 Flashcards (Revisão)", 
        "📝 Banco de Questões"
    ])

    # --- 1. ABA DE RESUMOS ---
    with tab_resumos:
        st.subheader("Seus Protocolos Salvos")
        try:
            # Filtro rigoroso pela categoria 'Resumo'
            response = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            resumos = response.data if response.data else []
            
            if not resumos:
                st.info("Nenhum resumo encontrado. Salve protocolos através do Core AI.")
            else:
                for r in resumos:
                    if isinstance(r, dict):
                        with st.container(border=True):
                            c1, c2 = st.columns([0.9, 0.1])
                            c1.markdown(f"**{r.get('pergunta', 'Sem Título')}**")
                            if c2.button("🗑️", key=f"del_res_{r['id']}"):
                                mover_para_lixeira(r['id'])
                                st.rerun()
                            
                            with st.expander("Ler Protocolo Completo"):
                                st.markdown(r.get('resposta', 'Sem conteúdo disponível.'))
                                st.caption(f"Área: {r.get('grande_area', 'Geral')}")
        except Exception as e:
            st.error(f"Erro ao carregar resumos: {e}")

    # --- 2. ABA DE FLASHCARDS ---
    with tab_cards:
        st.subheader("Revisão Ativa (SM-2)")
        try:
            todos_cards = listar_flashcards(email)
            # Filtra apenas o que for categoria Flashcard
            cards = [c for c in todos_cards if isinstance(c, dict) and c.get('categoria') == 'Flashcard']
            
            if not cards:
                st.info("Você não possui flashcards pendentes.")
            else:
                for card in cards:
                    with st.expander(f"🎴 {str(card.get('pergunta'))[:60]}..."):
                        st.markdown(f"**Pergunta:** {card.get('pergunta')}")
                        st.divider()
                        st.markdown(f"**Resposta:** {card.get('resposta')}")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        if col1.button("🟢 Fácil", key=f"f_{card['id']}"): 
                            atualizar_progresso_sm2(card['id'], 5)
                            st.success("Agendado!")
                        if col2.button("🟡 Médio", key=f"m_{card['id']}"): 
                            atualizar_progresso_sm2(card['id'], 3)
                            st.warning("Revisão em breve.")
                        if col3.button("🔴 Difícil", key=f"d_{card['id']}"): 
                            atualizar_progresso_sm2(card['id'], 1)
                            st.error("Revisão urgente.")
                        if col4.button("🗑️", key=f"del_c_{card['id']}"):
                            mover_para_lixeira(card['id'])
                            st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar flashcards: {e}")

    # --- 3. ABA DE QUESTÕES ---
    with tab_questoes:
        st.subheader("Treinamento de Questões")
        try:
            questoes = listar_questoes(email)
            if not questoes:
                st.info("Nenhuma questão gerada até o momento.")
            else:
                for i, q in enumerate(questoes):
                    if isinstance(q, dict):
                        with st.container(border=True):
                            st.markdown(f"**Questão {i+1}:** {q.get('pergunta')}")
                            
                            alternativas = {
                                "A": q.get('opcao_a'),
                                "B": q.get('opcao_b'),
                                "C": q.get('opcao_c'),
                                "D": q.get('opcao_d')
                            }
                            
                            escolha = st.radio(f"Selecione a resposta ({i+1}):", 
                                             options=["A", "B", "C", "D"], 
                                             format_func=lambda x: f"{x}) {alternativas[x]}",
                                             key=f"q_radio_{q['id']}")
                            
                            if st.button("Validar Resposta", key=f"btn_q_{q['id']}"):
                                if escolha == q.get('gabarito'):
                                    st.success(f"Correto! Alternativa {escolha}")
                                else:
                                    st.error(f"Incorreto. O gabarito correto é {q.get('gabarito')}")
                                st.info(f"**Justificativa:** {q.get('explica_correta')}")
        except Exception as e:
            st.error(f"Erro ao carregar questões: {e}")

