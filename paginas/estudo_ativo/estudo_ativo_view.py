import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta

# Conexão segura com o Banco
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def show():
    st.title("📚 Master Study | Curva de Esquecimento")
    st.subheader(f"Plano de Revisão: Semana de {datetime.now().strftime('%d/%m')}")

    # 1. BUSCAR HISTÓRICO REAL NO SUPABASE
    try:
        res = supabase.table("resultados_performance").select("*").eq("user_email", st.session_state.user_email).execute()
        df = pd.DataFrame(res.data)

        if df.empty:
            st.info("Você ainda não tem histórico de estudos. Comece respondendo aos simulados para gerar dados!")
        else:
            # 2. LÓGICA DE PRIORIZAÇÃO (CURVA DE ESQUECIMENTO)
            # Prioridade 1: Temas com acerto < 70%
            # Prioridade 2: Temas estudados há mais de 7 dias
            
            st.markdown("### 🔥 Prioridades de Revisão")
            
            # Simulando cálculo de prioridade baseada em performance
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            revisoes = df.sort_values(by=['aproveitamento_percent', 'data_hora'], ascending=[True, True])

            for _, row in revisoes.head(5).iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**Tema:** {row.get('categoria_foco', 'Geral')}")
                        st.write(f"Último desempenho: {row['aproveitamento_percent']}%")
                    with c2:
                        st.button("Revisar Agora", key=f"rev_{row['id']}")

    except Exception as e:
        st.error("Não foi possível carregar seu histórico. Verifique a conexão com o Supabase.")

    # 3. INTERFACE DE ESTUDO ATIVO (FLASHCARDS)
    st.divider()
    st.markdown("### 🗂️ Seus Flashcards Recentes")
    # Busca na tabela de flashcards que criamos no SQL único
    res_cards = supabase.table("flashcards").select("*").execute()
    if res_cards.data:
        for card in res_cards.data[:3]:
            with st.expander(f"Pergunta: {card['pergunta']}"):
                st.write(f"**Resposta:** {card['resposta']}")
                st.caption(f"Categoria: {card['categoria']}")
