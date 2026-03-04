import streamlit as st
from database import get_supabase, listar_flashcards, listar_questoes, mover_para_lixeira, atualizar_progresso_sm2

def show():
    st.title("🎓 Master Study Hub")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    t_res, t_cards, t_qs = st.tabs(["📘 Resumos", "🎴 Flashcards", "📝 Questões"])

    with t_res:
        try:
            res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            for r in [i for i in res.data if isinstance(i, dict)]:
                with st.container(border=True):
                    st.subheader(r.get('pergunta'))
                    with st.expander("Ler"): st.markdown(r.get('resposta'))
                    if st.button("🗑️", key=f"dr_{r['id']}"): mover_para_lixeira(r['id']); st.rerun()
        except: st.info("Sem resumos.")

    with t_cards:
        cards = [c for c in listar_flashcards(email) if isinstance(c, dict) and c.get('categoria') == 'Flashcard']
        for c in cards:
            with st.expander(f"🎴 {str(c.get('pergunta'))[:50]}..."):
                st.write(c.get('resposta'))
                c1, c2, c3 = st.columns(3)
                if c1.button("🟢 Fácil", key=f"f_{c['id']}"): atualizar_progresso_sm2(c['id'], 5)
                if c2.button("🔴 Difícil", key=f"d_{c['id']}"): atualizar_progresso_sm2(c['id'], 1)
                if c3.button("🗑️", key=f"delc_{c['id']}"): mover_para_lixeira(c['id']); st.rerun()

    with t_qs:
        qs = [q for q in listar_questoes(email) if isinstance(q, dict)]
        for i, q in enumerate(qs):
            with st.container(border=True):
                st.write(f"**{i+1}. {q.get('pergunta')}**")
                escolha = st.radio("Opções:", ["A","B","C","D"], key=f"q_{q['id']}")
                if st.button("Validar", key=f"v_{q['id']}"):
                    if escolha == q.get('gabarito'): st.success("Correto!")
                    else: st.error(f"Gabarito: {q.get('gabarito')}")
