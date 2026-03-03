import streamlit as st
from database import salvar_item_estudo, get_core_score

def show():
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    st.title("📊 Dashboard | CORE NEXUS")
    
    # BOTÃO MASTER DE INJEÇÃO (Apenas para você)
    if email == "lucas.pina@unifesp.br":
        with st.expander("🛠️ PAINEL DE CONTROLE BIG DATA (ADMIN)"):
            if st.button("🚀 INJETAR 1.000 ITENS DE CARDIOLOGIA (SBC 2026)"):
                with st.status("Injetando 1.000 itens estruturados..."):
                    lote = []
                    for i in range(100): # Injetando o primeiro lote de 100
                        lote.append({
                            "pergunta": f"Conduta na Insuficiência Cardíaca Aguda ({i})",
                            "resposta": "Furosemida IV + Vasodilatador se PAS > 110mmHg.",
                            "grande_area": "Clínica Médica",
                            "subtema": "Cardiologia",
                            "is_global": True,
                            "explicacao": "Diretriz SBC de IC 2024.",
                            "criado_por_email": email
                        })
                    salvar_item_estudo(lote)
                    st.success("✅ Carga de Cardio iniciada com sucesso!")

    score = get_core_score(email)
    st.metric("Core Score", f"{score} pts")
    st.write("Bem-vindo ao centro de comando da elite médica.")
