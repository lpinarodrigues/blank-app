import streamlit as st
import pandas as pd
from database import salvar_flashcard, listar_flashcards, atualizar_revisao_card
from utils.ia_engine import gerar_cards_cloze
from utils.audio_engine import alertar_seguranca_voce # Reutilizando motor ElevenLabs

def show():
    st.markdown("### 🧬 Master Study | Global Elite Edition")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    aba1, aba2 = st.tabs(["🔥 Sessão de Estudo", "🧪 Laboratório de Cards"])

    with aba1:
        cards = listar_flashcards(email)
        if not cards:
            st.info("Deck vazio. Gere novos cards no Laboratório!")
        else:
            # Seleção de Card com Algoritmo de Repetição
            card = cards[0] 
            
            with st.container(border=True):
                st.caption(f"Categoria: {card.get('categoria', 'Geral')}")
                st.subheader(card['pergunta']) # Aqui entra o Cloze [...]
                
                col_audio, col_reveal = st.columns([1, 4])
                with col_audio:
                    if st.button("🔊 Ouvir"):
                        audio = alertar_seguranca_voce(card['pergunta'])
                        if audio: st.audio(audio)
                
                with col_reveal:
                    if st.button("Revelar Resposta (Espaço)", use_container_width=True):
                        st.markdown(f"### ✅ {card['resposta']}")
                        st.info(f"💡 Dica Clínica: {card.get('explicacao', 'Consulte a diretriz SBC 2024.')}")
                        
                        st.divider()
                        st.markdown("Qual seu nível de domínio?")
                        qualidades = [("Esqueci (1d)", 1), ("Difícil (3d)", 3), ("Bom (7d)", 4), ("Fácil (15d)", 5)]
                        cols = st.columns(4)
                        for i, (label, val) in enumerate(qualidades):
                            if cols[i].button(label):
                                atualizar_revisao_card(card['id'], val)
                                st.rerun()

    with aba2:
        st.subheader("Gerador de Cloze Deletion (USMLE Style)")
        tema_input = st.text_input("Tema:", placeholder="Ex: Choque Cardiogênico")
        if st.button("Gerar 5 Cards de Alta Retenção ⚡"):
            novos_cards = gerar_cards_cloze(tema_input)
            for nc in novos_cards:
                salvar_flashcard(nc['texto_omissao'], nc['resposta'], tema_input, email)
            st.success(f"{len(novos_cards)} cards adicionados ao seu cérebro digital.")
