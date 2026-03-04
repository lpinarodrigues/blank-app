import streamlit as st
from database import listar_flashcards, mover_para_lixeira, atualizar_progresso_sm2

def show():
    st.markdown("### 🎴 Meus Flashcards")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    cards = [c for c in listar_flashcards(email) if c.get('categoria') == 'Flashcard']
    
    if not cards:
        st.info("Sua coleção está vazia.")
        return

    for card in cards:
        if isinstance(card, dict):
            with st.expander(f"Q: {str(card.get('pergunta'))[:50]}..."):
                st.write(card.get('resposta'))
                c1, c2, c3, c4 = st.columns([1,1,1,1])
                if c1.button("🟢 Fácil", key=f"f_{card['id']}"): atualizar_progresso_sm2(card['id'], 5)
                if c4.button("🗑️", key=f"d_{card['id']}"): mover_para_lixeira(card['id']); st.rerun()
