import streamlit as st
from supabase import create_client, Client

url: str = "https://svejzpsygmjgscjwwmzz.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2ZWp6cHN5Z21qZ3Njand3bXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzNzgyNzMsImV4cCI6MjA4Njk1NDI3M30.3UnmqMgRG01vEo2LT3hSTuIlqzUZw_DVHolj6l_hALM"
supabase: Client = create_client(url, key)

def show():
    st.title("👤 Gestão & Auditoria | CORE NEXUS")
    is_adm = st.session_state.get('user_email') == "lucas.pina@unifesp.br"

    if is_adm:
        st.subheader("🔑 Painel de Auditoria Central")
        tab1, tab2 = st.tabs(["👥 Homologação", "📊 Estatísticas"])
        
        with tab1:
            res = supabase.table("usuarios").select("*").eq("aprovado", False).execute()
            pendentes = res.data
            
            if not pendentes:
                st.info("Nenhuma solicitação pendente no momento.")
            else:
                for user in pendentes:
                    with st.container(border=True):
                        col_i, col_b = st.columns([3, 1])
                        with col_i:
                            st.write(f"**{user['nome']}** ({user['vinculo']})")
                            st.caption(f"E-mail: {user['email']} | Tel: {user['tel']}")
                        with col_b:
                            if st.button("✅ Aprovar", key=f"app_{user['id']}"):
                                supabase.table("usuarios").update({"aprovado": True}).eq("id", user['id']).execute()
                                st.rerun()
                            if st.button("❌ Negar", key=f"neg_{user['id']}"):
                                supabase.table("usuarios").delete().eq("id", user['id']).execute()
                                st.rerun()
    else:
        st.write(f"Usuário: {st.session_state.user_email}")
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()
