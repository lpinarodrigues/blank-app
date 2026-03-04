import streamlit as st
import os

# Configuração de Página - DEVE ser o primeiro comando Streamlit
st.set_page_config(page_title="CORE NEXUS", page_icon="🧠", layout="wide")

# Função para carregar módulos com segurança
def carregar_modulo(caminho):
    try:
        if "core_ai" in caminho:
            from paginas.core_ai import core_ai_view
            return core_ai_view
        elif "estudo" in caminho:
            from paginas.estudo import master_study_view
            return master_study_view
    except Exception as e:
        st.error(f"Erro ao carregar módulo {caminho}: {e}")
        return None

def main():
    st.sidebar.title("NEXUS CORE")
    
    # Verificação de Chaves (Para diagnóstico)
    if "SUPABASE_URL" not in st.secrets:
        st.error("ERRO: Chaves de segredo não encontradas no Streamlit Cloud!")
        st.stop()

    menu = st.sidebar.selectbox("Navegação:", ["🧠 Terminal Clínico", "🎓 Master Study"])
    
    if menu == "🧠 Terminal Clínico":
        modulo = carregar_modulo("core_ai")
        if modulo: modulo.show()
    else:
        modulo = carregar_modulo("estudo")
        if modulo: modulo.show()

if __name__ == "__main__":
    main()
