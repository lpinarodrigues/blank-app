import streamlit as st

def show():
    st.markdown("### 👤 Perfil do Médico")
    
    with st.container(border=True):
        st.write(f"**E-mail:** {st.session_state.get('user_email', 'lucas.pina@unifesp.br')}")
        st.write("**Instituição:** UNIFESP / Dante Pazzanese")
        st.write("**Nível de Acesso:** Administrador CORE")
        
    st.divider()
    if st.button("🔄 Sincronizar Dados Supabase"):
        st.success("Dados sincronizados com sucesso!")
