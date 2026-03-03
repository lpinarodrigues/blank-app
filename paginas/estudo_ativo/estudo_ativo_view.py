import streamlit as st
import pandas as pd
from database import listar_flashcards, atualizar_revisao_card, obter_estatisticas_estudo, sugerir_foco_ia
import time

def show():
    st.markdown("### 🧬 Master Study | Padrão Ouro Internacional")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    # --- BARRA DE PROGRESSO DE RETENÇÃO ---
    df_stats = obter_estatisticas_estudo(email)
    if not df_stats.empty:
        progresso = (df_stats[df_stats['facilidade'] > 2.5].shape[0] / df_stats.shape[0]) * 100
        st.write(f"**Nível de Retenção de Longo Prazo:** {progresso:.1f}%")
        st.progress(progresso / 100)
        
        tema_foco = sugerir_foco_ia(df_stats)
        st.warning(f"🎯 **Sugestão da IA:** O teu rendimento em `{tema_foco}` está abaixo da média. Que tal revisar agora?")

    st.divider()

    # --- MODO DE ESTUDO FLUIDO (UX BRAINSCAPE) ---
    tab_estudo, tab_config = st.tabs(["🔥 Sessão Ativa", "⚙️ Gerir Decks"])

    with tab_estudo:
        cards = listar_flashcards(email)
        # Filtro de Repetição Espaçada Real
        hoje = pd.Timestamp.now().date()
        cards_revisar = [c for c in cards if pd.to_datetime(c.get('proxima_revisao', '2000-01-01')).date() <= hoje]
        
        if not cards_revisar:
            st.success("🎉 Cérebro em Dia! Não tens revisões pendentes para hoje.")
            if st.button("Forçar Modo 'Cramming' (Estudar tudo)"):
                cards_revisar = cards
            else: return

        # O Card Atual
        card = cards_revisar[0]
        
        # Interface de Card "Clean"
        with st.container(border=True):
            st.caption(f"Deck: {card['categoria']} | Revisões: {card.get('revisões_totais', 0)}")
            st.markdown(f"## {card['pergunta']}")
            
            if "revelado" not in st.session_state: st.session_state.revelado = False
            
            if not st.session_state.revelado:
                if st.button("MOSTRAR RESPOSTA (ENTER)", use_container_width=True):
                    st.session_state.revelado = True
                    st.rerun()
            else:
                st.markdown(f"### ✅ {card['resposta']}")
                st.info(f"**Explicação Técnica:** {card.get('explicacao', 'Baseado nas últimas diretrizes.')}")
                
                st.divider()
                st.write("Qual foi o teu esforço de memória?")
                cols = st.columns(5)
                # Escala de 1 a 5 (Padrão SuperMemo)
                for i in range(1, 6):
                    if cols[i-1].button(f"{i}", help=f"1=Esqueci, 5=Perfeito"):
                        atualizar_revisao_card(card['id'], i)
                        st.session_state.revelado = False
                        st.toast(f"Card agendado! +{i*5} pts", icon="🧠")
                        time.sleep(0.5)
                        st.rerun()

    with tab_config:
        st.subheader("Configurações do Algoritmo")
        st.toggle("Ativar Áudio Automático (ElevenLabs)")
        st.toggle("Modo USMLE (Apenas Inglês/Português)")
        if st.button("Limpar Histórico de Revisão"):
            st.error("Ação irreversível. Tens a certeza?")
