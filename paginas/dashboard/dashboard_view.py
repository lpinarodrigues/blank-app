import streamlit as st
from database import get_core_score, listar_lixeira, restaurar_da_lixeira, esvaziar_lixeira

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    st.title("📊 Painel de Controlo | CORE NEXUS")
    
    score = get_core_score(email)
    st.metric("Core Score", f"{score} pts")
    
    st.divider()
    
    # --- SISTEMA DE LIXEIRA (RECICLAGEM) ---
    with st.expander("🗑️ Gestão da Lixeira (Reciclagem)", expanded=False):
        st.write("Os itens eliminados são guardados aqui por segurança.")
        itens_lixeira = listar_lixeira(email)
        
        if itens_lixeira:
            col_info, col_btn = st.columns([3, 1])
            col_info.warning(f"Existem {len(itens_lixeira)} itens na sua lixeira.")
            
            if col_btn.button("🔥 Esvaziar Tudo", type="primary"):
                esvaziar_lixeira(email)
                st.toast("Lixeira limpa definitivamente!")
                st.rerun()
                
            st.divider()
            
            for item in itens_lixeira:
                c1, c2 = st.columns([4, 1])
                c1.write(f"📄 {str(item.get('pergunta', 'Sem título'))[:60]}...")
                if c2.button("Restaurar ♻️", key=f"restaurar_{item.get('id', 'x')}"):
                    restaurar_da_lixeira(item['id'])
                    st.rerun()
        else:
            st.success("✨ A sua lixeira está completamente vazia.")
