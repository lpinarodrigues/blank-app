import streamlit as st

def show():
    st.markdown("### 📊 Painel de Controle | CORE NEXUS")
    
    # Cards de Performance Superior
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Core Score", "850 pts", "+15")
    with c2:
        st.metric("Retenção", "94%", "2%")
    with c3:
        st.metric("Meta Diária", "12/15", "80%")

    st.divider()

    # Layout de Atividades Recentes
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("📝 Atividade de Estudo")
        st.write("Último Simulado: **Cardiologia Clínica (Dante)**")
        st.progress(0.85, text="85% concluído")
        
    with col_side:
        st.subheader("🔔 Alertas")
        st.warning("Revisão de Valvopatias expira em 2h.")
