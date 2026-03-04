import streamlit as st
from database import get_supabase, listar_flashcards, listar_questoes, mover_para_lixeira, atualizar_progresso_sm2
from datetime import datetime

def show():
    st.title("🎓 Master Study Hub | Performance Médica")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    # CSS para os Cards
    st.markdown("""
        <style>
        .flashcard-box {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #3b82f6;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    t_res, t_cards, t_qs = st.tabs(["📘 Meus Protocolos", "🎴 Revisão Ativa", "📝 Simulados ABCD"])

    # --- ABA 1: PROTOCOLOS (RESUMOS) ---
    with t_res:
        st.subheader("📚 Biblioteca de Protocolos")
        try:
            res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
            itens = [i for i in res.data if isinstance(i, dict)]
            if not itens:
                st.info("Sua biblioteca está vazia. Gere um resumo no Core AI!")
            else:
                for r in itens:
                    with st.container(border=True):
                        c1, c2 = st.columns([0.9, 0.1])
                        c1.markdown(f"### {r.get('pergunta')}")
                        if c2.button("🗑️", key=f"del_res_{r['id']}"):
                            mover_para_lixeira(r['id'])
                            st.rerun()
                        st.caption(f"🏷️ {r.get('grande_area')} | {r.get('subtema')}")
                        with st.expander("Expandir Conteúdo Clínico"):
                            st.markdown(r.get('resposta'))
        except: st.error("Erro ao conectar com a Biblioteca.")

    # --- ABA 2: FLASHCARDS (EQUIPADOS COM SM-2) ---
    with t_cards:
        st.subheader("🎴 Sistema de Repetição Espaçada")
        cards = [c for c in listar_flashcards(email) if isinstance(c, dict) and c.get('categoria') == 'Flashcard']
        
        if not cards:
            st.info("Nenhum flashcard pendente para hoje.")
        else:
            st.progress(100, text="Meta de Revisão Diária")
            for c in cards:
                with st.container(border=True):
                    st.markdown(f"**Pergunta:**\n{c.get('pergunta')}")
                    
                    with st.expander("Revelar Resposta"):
                        st.markdown(f"**Resposta:**\n{c.get('resposta')}")
                        st.divider()
                        st.caption("Como foi sua facilidade em lembrar?")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        if col1.button("🟢 Fácil", key=f"f_{c['id']}"):
                            atualizar_progresso_sm2(c['id'], 5)
                            st.toast("Revisão agendada para daqui a 4 dias!")
                        if col2.button("🟡 Médio", key=f"m_{c['id']}"):
                            atualizar_progresso_sm2(c['id'], 3)
                            st.toast("Revisão agendada para amanhã!")
                        if col3.button("🔴 Difícil", key=f"d_{c['id']}"):
                            atualizar_progresso_sm2(c['id'], 1)
                            st.toast("Repetir em 10 minutos!")
                        if col4.button("🗑️", key=f"del_c_{c['id']}"):
                            mover_para_lixeira(c['id'])
                            st.rerun()

    # --- ABA 3: QUESTÕES (SIMULADO) ---
    with t_qs:
        st.subheader("📝 Banco de Questões Estilo Prova")
        qs = [q for q in listar_questoes(email) if isinstance(q, dict)]
        if not qs:
            st.info("Gere questões no Core AI para treinar aqui.")
        else:
            for i, q in enumerate(qs):
                with st.container(border=True):
                    st.markdown(f"**{i+1}. {q.get('pergunta')}**")
                    opcoes = ["A", "B", "C", "D"]
                    alt_text = [q.get('opcao_a'), q.get('opcao_b'), q.get('opcao_c'), q.get('opcao_d')]
                    
                    escolha = st.radio(f"Selecione sua resposta para a Q{i+1}:", 
                                     options=opcoes, 
                                     format_func=lambda x: f"{x}) {alt_text[opcoes.index(x)]}",
                                     key=f"q_rad_{q['id']}")
                    
                    if st.button("Confirmar Gabarito", key=f"check_{q['id']}"):
                        if escolha == q.get('gabarito'):
                            st.success(f"Correto! Alternativa {escolha}")
                        else:
                            st.error(f"Incorreto. O gabarito é {q.get('gabarito')}")
                        st.info(f"**Justificativa:** {q.get('explica_correta')}")

