import streamlit as st

def show():
    st.title("🔮 O Oráculo | Inteligência de Decisão")
    st.markdown("---")

    fluxo = st.sidebar.radio("Algoritmo de Decisão:", 
                            ["Dor Torácica / SCA", "Arritmias Agudas", "Choque / Hipotensão", "Síncope"])

    if fluxo == "Dor Torácica / SCA":
        st.header("🚑 Protocolo de Dor Torácica")
        st.info("Diretriz SBC/ESC: Decisão de Reperfusão e Estratificação.")
        
        col1, col2 = st.columns(2)
        com_supra = col1.button("🚨 ECG com SUPRA de ST")
        sem_supra = col2.button("📉 ECG SEM SUPRA / Infradesnivelamento")

        if com_supra:
            st.error("### CONDUTA: REPERFUSÃO IMEDIATA")
            st.markdown("""
            1. **Tempo porta-balão < 90 min?** -> Angioplastia Primária.
            2. **Tempo porta-balão > 120 min?** -> Trombólise (se < 12h de sintomas).
            3. **AAS (300mg) + Clopidogrel (600mg ou 300mg se >75 anos).**
            4. **Heparina (HNF ou Enoxaparina).**
            """)
        
        if sem_supra:
            st.warning("### ESTRATIFICAÇÃO DE RISCO")
            st.write("Calcular GRACE Score no módulo 'Core Scores' para definir tempo de CATE (Imediato, 24h ou 72h).")

    elif fluxo == "Arritmias Agudas":
        st.header("💓 Manejo de Arritmias (ACLS)")
        estavel = st.radio("Paciente Estável?", ["Sim", "Não (Instabilidade Hemodinâmica)"])
        
        if estavel == "Não (Instabilidade Hemodinâmica)":
            st.error("🚨 **CONDUTA:** Cardioversão Elétrica Sincronizada imediata.")
        else:
            st.success("✅ **CONDUTA:** Manobras vagais ou Adenosina (se TSV) / Controle de frequência (se FA).")

