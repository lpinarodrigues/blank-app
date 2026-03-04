import streamlit as st
from database import get_supabase, mover_para_lixeira, atualizar_progresso_sm2

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # ---------------------------------------------------------
    # 📱 CSS MOBILE-FIRST (Estilo iOS/Android App)
    # ---------------------------------------------------------
    st.markdown("""
        <style>
        /* Ajuste de margens para telas pequenas */
        .block-container { padding-top: 2rem; max-width: 800px; }
        
        /* O 'Cartão' principal (Mobile UX) */
        .mobile-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 24px; /* Bordas bem arredondadas estilo Apple */
            padding: 40px 20px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
            text-align: center;
            margin-bottom: 24px;
        }
        
        .mc-pergunta { font-size: 1.4rem; font-weight: 800; color: #f8fafc; line-height: 1.4; margin-bottom: 10px; }
        .mc-resposta { font-size: 1.2rem; color: #10b981; font-weight: 600; padding-top: 20px; border-top: 1px solid #334155; margin-top: 20px; }
        
        /* Botões mais altos (Touch-friendly) */
        .stButton>button { border-radius: 16px; height: 54px; font-weight: 700; font-size: 1.1rem; }
        </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 🧠 GESTÃO DE ESTADO (MEMÓRIA DO CARROSSEL)
    # ---------------------------------------------------------
    if 'card_index' not in st.session_state: st.session_state.card_index = 0
    if 'show_answer' not in st.session_state: st.session_state.show_answer = False

    st.markdown("<h2 style='text-align: center; font-size: 1.8rem;'>🎓 Master Study</h2>", unsafe_allow_html=True)
    st.divider()

    t_cards, t_qs, t_res = st.tabs(["⚡ Flashcards", "📝 Simulados", "📘 Protocolos"])

    # --- ABA 1: FLASHCARDS (MODO FOCO 1 POR VEZ) ---
    with t_cards:
        try:
            res_cards = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Flashcard").neq("categoria", "Lixeira").execute()
            cards = res_cards.data if res_cards.data else []
            
            if not cards:
                st.success("🎉 Parabéns! Você zerou suas revisões de hoje!")
                st.balloons()
            else:
                # Segurança: se o index passar do limite (ex: apagou cards), reseta
                if st.session_state.card_index >= len(cards):
                    st.session_state.card_index = 0
                    st.session_state.show_answer = False
                
                c_atual = cards[st.session_state.card_index]
                
                # Barra de progresso mobile
                progresso = (st.session_state.card_index + 1) / len(cards)
                st.progress(progresso, text=f"Card {st.session_state.card_index + 1} de {len(cards)}")
                
                # Renderização do Card Único
                if not st.session_state.show_answer:
                    st.markdown(f"""
                        <div class="mobile-card">
                            <div class="mc-pergunta">{c_atual.get('pergunta')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Revelar Resposta 👁️", use_container_width=True, type="primary"):
                        st.session_state.show_answer = True
                        st.rerun()
                
                else:
                    st.markdown(f"""
                        <div class="mobile-card">
                            <div class="mc-pergunta">{c_atual.get('pergunta')}</div>
                            <div class="mc-resposta">{c_atual.get('resposta')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.caption("Qual seu nível de retenção?")
                    c1, c2, c3 = st.columns(3)
                    
                    # Lógica de avanço de card
                    def proximo_card(id_card, peso):
                        atualizar_progresso_sm2(id_card, peso)
                        st.session_state.card_index += 1
                        st.session_state.show_answer = False
                    
                    if c1.button("🟢 Fácil", use_container_width=True): 
                        proximo_card(c_atual['id'], 5); st.rerun()
                    if c2.button("🟡 Médio", use_container_width=True): 
                        proximo_card(c_atual['id'], 3); st.rerun()
                    if c3.button("🔴 Difícil", use_container_width=True): 
                        proximo_card(c_atual['id'], 1); st.rerun()

        except Exception as e: st.error(f"Erro: {e}")

    # --- ABA 2: QUESTÕES ---
    with t_qs:
        try:
            res_qs = get_supabase().table("questionarios").select("*").eq("criado_por_email", email).execute()
            qs = res_qs.data if res_qs.data else []
            
            if not qs: st.info("Gere simulados no Core AI.")
            else:
                for i, q in enumerate(qs):
                    if isinstance(q, dict):
                        with st.container(border=True):
                            st.markdown(f"**Q{i+1}.** {q.get('pergunta')}")
                            opcoes = ["A", "B", "C", "D"]
                            alt_text = [q.get('opcao_a', ''), q.get('opcao_b', ''), q.get('opcao_c', ''), q.get('opcao_d', '')]
                            escolha = st.radio("Sua resposta:", options=opcoes, format_func=lambda x: f"{x}) {alt_text[opcoes.index(x)]}", key=f"q_{q.get('id', i)}", label_visibility="collapsed")
                            if st.button("Checar", key=f"chk_{q.get('id', i)}"):
                                if escolha == q.get('gabarito'): st.success("🎯 Correto!")
                                else: st.error(f"❌ Gabarito: {q.get('gabarito')}")
                                st.info(q.get('explica_correta'))
        except: pass

    # --- ABA 3: PROTOCOLOS ---
    with t_res:
        try:
            res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            itens = res.data if res.data else []
            if not itens: st.info("Sem protocolos.")
            else:
                for r in itens:
                    if isinstance(r, dict):
                        with st.expander(f"📘 {r.get('pergunta')}"):
                            st.markdown(r.get('resposta'))
                            if st.button("🗑️ Excluir", key=f"d_r_{r.get('id')}"): mover_para_lixeira(r.get('id')); st.rerun()
        except: pass

