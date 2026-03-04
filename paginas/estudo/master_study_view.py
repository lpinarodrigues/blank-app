import streamlit as st
from database import get_supabase, listar_flashcards, listar_questoes, mover_para_lixeira, atualizar_progresso_sm2

def show():
    st.title("🎓 Master Study | Centro de Performance")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # Criação das Abas de Conexão
    tab_resumos, tab_cards, tab_simulados = st.tabs([
        "📘 Meus Resumos", 
        "🎴 Flashcards", 
        "📝 Questões"
    ])

    # --- CONEXÃO 1: RESUMOS (Filtra categoria 'Resumo') ---
    with tab_resumos:
        try:
            res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            resumos = [r for r in res.data if isinstance(r, dict)] if res.data else []
            
            if not resumos:
                st.info("Nenhum resumo salvo ainda.")
            else:
                for r in resumos:
                    with st.container(border=True):
                        col_t, col_d = st.columns([10, 1])
                        col_t.subheader(r.get('pergunta', 'Sem Título'))
                        if col_d.button("🗑️", key=f"dr_{r['id']}"):
                            mover_para_lixeira(r['id'])
                            st.rerun()
                        with st.expander("Ver Conteúdo"):
                            st.markdown(r.get('resposta', ''))
        except: st.error("Erro ao carregar resumos.")

    # --- CONEXÃO 2: FLASHCARDS (Filtra categoria 'Flashcard') ---
    with tab_cards:
        cards = [c for c in listar_flashcards(email) if c.get('categoria') == 'Flashcard']
        if not cards:
            st.info("Sua coleção de cards está vazia.")
        else:
            for c in cards:
                with st.expander(f"🎴 {str(c.get('pergunta'))[:60]}..."):
                    st.write(f"**P:** {c.get('pergunta')}")
                    st.divider()
                    st.write(f"**R:** {c.get('resposta')}")
                    c1, c2, c3 = st.columns(3)
                    if c1.button("🟢 Fácil", key=f"f_{c['id']}"): atualizar_progresso_sm2(c['id'], 5)
                    if c2.button("🟡 Médio", key=f"m_{c['id']}"): atualizar_progresso_sm2(c['id'], 3)
                    if c3.button("🔴 Difícil", key=f"d_{c['id']}"): atualizar_progresso_sm2(c['id'], 1)

    # --- CONEXÃO 3: QUESTÕES (Conecta com a tabela questionarios) ---
    with tab_simulados:
        questoes = listar_questoes(email)
        if not questoes:
            st.info("Nenhuma questão gerada.")
        else:
            for i, q in enumerate(questoes):
                with st.container(border=True):
                    st.markdown(f"**Questão {i+1}**")
                    st.write(q.get('pergunta'))
                    resp = st.radio("Escolha:", ["A", "B", "C", "D"], key=f"rad_{q['id']}")
                    if st.button("Check Gabarito", key=f"btn_{q['id']}"):
                        if resp == q.get('gabarito'): st.success("Correto!")
                        else: st.error(f"Errado. Gabarito: {q.get('gabarito')}")
                        st.caption(f"Justificativa: {q.get('explica_correta')}")
