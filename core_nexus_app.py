import streamlit as st
import sys
import os

# Configuração de Página - OBRIGATORIAMENTE o primeiro comando Streamlit
st.set_page_config(page_title="CORE NEXUS | Inteligência Médica", page_icon="🧠", layout="wide")

# Adiciona o diretório atual ao path para evitar erros de importação
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.sidebar.title("NEXUS CORE")
    
    # Verificação de Chaves (Para diagnóstico no log do Streamlit)
    if "SUPABASE_URL" not in st.secrets:
        st.error("🚨 Erro Crítico: Chaves de segredo (Secrets) não encontradas!")
        st.info("Verifique a aba 'Secrets' nas configurações do seu App no Streamlit Cloud.")
        st.stop()

    menu = st.sidebar.selectbox("Navegação:", ["🧠 Terminal Clínico AI", "🎓 Master Study Hub"])
    
    email = st.session_state.get('user_email', 'admin@nexus.com')
    st.sidebar.divider()
    st.sidebar.caption(f"🩺 Operador: {email}")

    # Roteamento Seguro
    try:
        if menu == "🧠 Terminal Clínico AI":
            from paginas.core_ai import core_ai_view
            core_ai_view.show()
        else:
            from paginas.estudo import master_study_view
            master_study_view.show()
    except Exception as e:
        st.error(f"Erro ao carregar módulo: {e}")
        st.info("Dica: Verifique se as pastas 'paginas/core_ai' e 'paginas/estudo' possuem o arquivo __init__.py")

if __name__ == "__main__":
    main()
