import os

FLASHCARDS_CODE = """import streamlit as st
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
"""

RESUMOS_CODE = """import streamlit as st
from database import get_supabase, mover_para_lixeira

def show():
    st.markdown("### 📘 Meus Resumos e Protocolos")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    try:
        res = get_supabase().table("flashcards").select("*").eq("criado_por_email", email).eq("categoria", "Resumo").neq("categoria", "Lixeira").execute()
        resumos = [i for i in res.data if isinstance(i, dict)] if res.data else []
    except: resumos = []

    if not resumos:
        st.info("Nenhum resumo salvo. Envie protocolos do Core AI para cá!")
        return

    for resumo in resumos:
        if isinstance(resumo, dict):
            t = str(resumo.get('pergunta', 'Resumo Sem Título')).replace('Resumo Oficial: ', '')
            c = str(resumo.get('resposta', 'Conteúdo vazio.'))
            a = str(resumo.get('grande_area', 'Geral'))
            rid = resumo.get('id', 0)
            
            with st.container(border=True):
                st.subheader(t)
                st.caption(f"🏷️ {a}")
                with st.expander("Ler Protocolo Completo"): st.markdown(c)
                if st.button("🗑️ Remover", key=f"del_res_{rid}"):
                    mover_para_lixeira(rid)
                    st.rerun()
"""

QUESTOES_CODE = """import streamlit as st
from database import listar_questoes

def show():
    st.markdown("### 📝 Banco de Questões")
    email = st.session_state.get('user_email', 'admin@nexus.com')
    questoes = listar_questoes(email)
    
    if not questoes or not isinstance(questoes, list):
        st.info("Nenhuma questão gerada. Use o Core AI para criar simulados!")
        return

    for i, q in enumerate(questoes):
        if isinstance(q, dict):
            p = str(q.get('pergunta', 'Erro na pergunta'))
            a = str(q.get('opcao_a', 'A')); b = str(q.get('opcao_b', 'B')); c = str(q.get('opcao_c', 'C')); d = str(q.get('opcao_d', 'D'))
            g = str(q.get('gabarito', 'A')); j = str(q.get('explica_correta', ''))
            
            with st.container(border=True):
                st.markdown(f"**{i+1}. {p}**")
                st.write(f"A) {a}"); st.write(f"B) {b}"); st.write(f"C) {c}"); st.write(f"D) {d}")
                with st.expander("Mostrar Gabarito e Justificativa"):
                    st.success(f"**Gabarito Correto: {g}**")
                    st.write(j)
"""

print("🔍 Iniciando varredura e rearranjo forçado...")

for root, dirs, files in os.walk('.'):
    # Ignora pastas de sistema do Python e do Git
    if '.git' in root or '__pycache__' in root: continue
    
    for file in files:
        # Pula os motores principais para não quebrá-ls
        if file.endswith('.py') and file not in ['force_rearrange.py', 'database.py', 'ia_engine.py', 'app.py', 'main.py']:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f: content = f.read()

                # Lógica do Rastreador: Procura palavras-chave para identificar de quem é o arquivo
                is_flashcards = ('listar_flashcards' in content) and ('st.' in content) and ('🎴' in content or 'atualizar_progresso' in content)
                is_resumos = ('Resumo' in content) and ('st.' in content) and ('📘' in content or 'Protocolo' in content) and ('listar_flashcards' not in content)
                is_questoes = ('listar_questoes' in content) and ('st.' in content) and ('📝' in content or 'Gabarito' in content)

                if is_flashcards:
                    with open(filepath, 'w', encoding='utf-8') as f: f.write(FLASHCARDS_CODE)
                    print(f"✅ SUBSTITUÍDO À FORÇA (Flashcards): {filepath}")
                elif is_resumos:
                    with open(filepath, 'w', encoding='utf-8') as f: f.write(RESUMOS_CODE)
                    print(f"✅ SUBSTITUÍDO À FORÇA (Resumos): {filepath}")
                elif is_questoes:
                    with open(filepath, 'w', encoding='utf-8') as f: f.write(QUESTOES_CODE)
                    print(f"✅ SUBSTITUÍDO À FORÇA (Questões): {filepath}")
            except Exception as e: pass

print("🚀 Varredura concluída!")
