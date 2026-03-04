import streamlit as st
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
