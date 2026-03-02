import streamlit as st
from supabase import create_client, Client

url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")
supabase = create_client(url, key)

def show():
    st.title("📚 Master Study")
    
    try:
        # Busca cards da biblioteca global
        res = supabase.table("flashcards").select("*").execute()
        
        if not res.data:
            st.info("Nenhum card encontrado. Crie o primeiro abaixo!")
        else:
            for card in res.data:
                with st.expander(f"❓ {card['pergunta']}"):
                    st.write(f"**Resposta:** {card['resposta']}")
                    st.caption(f"Categoria: {card['categoria']}")

    except Exception as e:
        st.error(f"Erro ao carregar cards: {e}")

    st.divider()
    with st.form("novo_card"):
        st.subheader("Novo Flashcard")
        p = st.text_input("Pergunta")
        r = st.text_area("Resposta")
        cat = st.selectbox("Categoria", ["Valvopatias", "Coronariopatia", "Arritmias", "IC"])
        if st.form_submit_button("Adicionar à Biblioteca"):
            supabase.table("flashcards").insert({"pergunta": p, "resposta": r, "categoria": cat}).execute()
            st.rerun()
