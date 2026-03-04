import streamlit as st
from database import listar_flashcards, mover_para_lixeira, atualizar_progresso_sm2

def show():
    st.markdown("### 🎴 Meus Flashcards")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    cards = listar_flashcards(email)
    
    if not cards or not isinstance(cards, list):
        st.info("Sua coleção de flashcards está vazia. Gere alguns no Core AI!")
        return

    for i, card in enumerate(cards):
        if isinstance(card, dict):
            p = card.get('pergunta', 'Pergunta indisponível')
            r = card.get('resposta', 'Resposta indisponível')
            cid = card.get('id', 0)
            
            with st.expander(f"Q: {str(p)[:80]}..."):
                st.markdown(f"**Pergunta:** {p}")
                st.markdown(f"**Resposta:** {r}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    c1, c2, c3 = st.columns(3)
                    if c1.button("🟢 Fácil", key=f"f_{cid}"): atualizar_progresso_sm2(cid, 5)
                    if c2.button("🟡 Médio", key=f"m_{cid}"): atualizar_progresso_sm2(cid, 3)
                    if c3.button("🔴 Difícil", key=f"d_{cid}"): atualizar_progresso_sm2(cid, 1)
                if col2.button("🗑️ Excluir", key=f"del_{cid}"):
                    mover_para_lixeira(cid)
                    st.rerun()
