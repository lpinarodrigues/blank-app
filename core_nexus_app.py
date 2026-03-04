import streamlit as st

# Configuração de Elite
st.set_page_config(page_title="CORE NEXUS", page_icon="🧠", layout="wide")

# Importação Consolidada
try:
    from paginas.core_ai import core_ai_view
    from paginas.estudo import master_study_view
except ImportError as e:
    st.error(f"Erro de carregamento de módulo: {e}")

def main():
    st.sidebar.title("NEXUS CORE")
    menu = st.sidebar.selectbox("Módulo:", ["🧠 Terminal Clínico", "🎓 Master Study Hub"])
    
    email = st.session_state.get('user_email', 'admin@nexus.com')
    st.sidebar.divider()
    st.sidebar.info(f"🩺 Operador: {email}")

    if menu == "🧠 Terminal Clínico":
        core_ai_view.show()
    elif menu == "🎓 Master Study Hub":
        master_study_view.show()

if __name__ == "__main__":
    main()
