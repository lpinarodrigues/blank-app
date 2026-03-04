import streamlit as st
from database import get_supabase, mover_para_lixeira, atualizar_progresso_sm2

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # ---------------------------------------------------------
    # 🎨 INJEÇÃO DE CSS PREMIUM (O SEGREDO DO VISUAL MODERNO)
    # ---------------------------------------------------------
    st.markdown("""
        <style>
        /* Esconde elementos padrão do Streamlit para visual mais limpo */
        .st-emotion-cache-16txtl3 { padding-top: 1rem; }
        
        /* Cards Premium */
        .nexus-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        .nexus-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
        
        /* Tags de Categoria */
        .nexus-tag {
            background: #3b82f633; color: #60a5fa;
            padding: 4px 12px; border-radius: 20px;
            font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
            letter-spacing: 0.5px; display: inline-block; margin-bottom: 12px;
        }
        
        /* Flashcards Tipografia */
        .fc-pergunta { font-size: 1.3rem; font-weight: 700; color: #f8fafc; text-align: center; margin-bottom: 10px; }
        .fc-resposta { font-size: 1.1rem; color: #94a3b8; text-align: center; padding-top: 15px; border-top: 1px dashed #334155; }
        
        /* Estilização das Abas */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0; padding: 10px 20px; font-weight: 600; }
        .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 🏆 DASHBOARD DE GAMIFICAÇÃO (TOPO)
    # ---------------------------------------------------------
    st.markdown("## 🎓 Centro de Performance")
    
    # Simulação de métricas reais (podemos conectar ao banco depois)
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("🔥 Ofensiva", "12 Dias", "Consistente")
    col_m2.metric("🎴 Cards Revisados", "45", "Hoje")
    col_m3.metric("🎯 Precisão em Questões", "82%", "+5% essa semana")
    
    st.divider()

    # ---------------------------------------------------------
    # 📂 ABAS MODERNIZADAS
    # ---------------------------------------------------------
    t_res, t_cards, t_qs = st.tabs(["📘 Biblioteca de Protocolos", "⚡ Modo Foco (Flashcards)", "📝 Arena de Simulados"])

    # --- ABA 1: PROTOCOLOS ---
    with t_res:
        try:
            res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            itens = res.data if res.data else []
            if not itens:
                st.info("Sua biblioteca está limpa. Adicione protocolos via Core AI.")
            else:
                for r in itens:
                    if isinstance(r, dict):
                        # HTML Customizado para o Card de Resumo
                        st.markdown(f"""
                            <div class="nexus-card">
                                <span class="nexus-tag">{r.get('grande_area', 'Clínica')}</span>
                                <span class="nexus-tag" style="background: #10b98133; color: #34d399;">{r.get('subtema', 'Geral')}</span>
                                <h3>{r.get('pergunta')}</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Os botões nativos precisam ficar fora do HTML
                        c1, c2 = st.columns([0.85, 0.15])
                        with c1:
                            with st.expander("Ler Protocolo Completo"):
                                st.write(r.get('resposta'))
                        with c2:
                            if st.button("🗑️ Excluir", key=f"del_res_{r.get('id')}"):
                                mover_para_lixeira(r.get('id'))
                                st.rerun()
        except Exception as e: st.error(f"Erro: {e}")

    # --- ABA 2: FLASHCARDS (ESTILO ANKI PREMIUM) ---
    with t_cards:
        try:
            res_cards = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Flashcard").neq("categoria", "Lixeira").execute()
            cards = res_cards.data if res_cards.data else []
            
            if not cards:
                st.success("🎉 Você zerou suas revisões de hoje!")
            else:
                st.progress(len(cards) / 100 if len(cards) < 100 else 1.0, text=f"{len(cards)} cards pendentes")
                
                for c in cards:
                    if isinstance(c, dict):
                        st.markdown(f"""
                            <div class="nexus-card">
                                <div class="fc-pergunta">{c.get('pergunta')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("👁️ Revelar Resposta"):
                            st.markdown(f"<div class='fc-resposta'>{c.get('resposta')}</div>", unsafe_allow_html=True)
                            st.write("") # Espaçamento
                            c1, c2, c3, c4 = st.columns(4)
                            if c1.button("🟢 Fácil (4d)", key=f"f_{c.get('id')}", use_container_width=True): atualizar_progresso_sm2(c.get('id'), 5); st.rerun()
                            if c2.button("🟡 Médio (1d)", key=f"m_{c.get('id')}", use_container_width=True): atualizar_progresso_sm2(c.get('id'), 3); st.rerun()
                            if c3.button("🔴 Difícil (10m)", key=f"d_{c.get('id')}", use_container_width=True): atualizar_progresso_sm2(c.get('id'), 1); st.rerun()
                            if c4.button("🗑️ Descartar", key=f"del_c_{c.get('id')}", use_container_width=True): mover_para_lixeira(c.get('id')); st.rerun()
                        st.write("---")
        except Exception as e: st.error(f"Erro: {e}")

    # --- ABA 3: QUESTÕES (ESTILO UWORLD) ---
    with t_qs:
        try:
            res_qs = get_supabase().table("questionarios").select("*").eq("criado_por_email", email).execute()
            qs = res_qs.data if res_qs.data else []
            
            if not qs:
                st.info("O banco de questões está vazio. Gere simulados no Core AI.")
            else:
                for i, q in enumerate(qs):
                    if isinstance(q, dict):
                        with st.container(border=True):
                            st.markdown(f"#### Questão {i+1}")
                            st.markdown(f"<p style='font-size: 1.1rem; color: #e2e8f0;'>{q.get('pergunta')}</p>", unsafe_allow_html=True)
                            
                            opcoes = ["A", "B", "C", "D"]
                            alt_text = [q.get('opcao_a', ''), q.get('opcao_b', ''), q.get('opcao_c', ''), q.get('opcao_d', '')]
                            
                            escolha = st.radio("Selecione sua resposta:", options=opcoes, format_func=lambda x: f"{x}) {alt_text[opcoes.index(x)]}", key=f"q_rad_{q.get('id', i)}", label_visibility="collapsed")
                            
                            if st.button("Validar Gabarito", key=f"check_{q.get('id', i)}", type="primary"):
                                if escolha == q.get('gabarito'): 
                                    st.success(f"🎯 **Correto!** Alternativa {escolha}")
                                else: 
                                    st.error(f"❌ **Incorreto.** O gabarito é a letra **{q.get('gabarito')}**")
                                
                                st.info(f"**📚 Justificativa Clínica:**\n{q.get('explica_correta')}")
        except Exception as e: st.error(f"Erro: {e}")

