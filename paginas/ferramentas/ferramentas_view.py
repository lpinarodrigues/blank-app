import streamlit as st
import google.generativeai as genai
from utils.ia_engine import consultar_core_ia_avancado

def calculadora_renal(peso, idade, creat, sexo):
    # Cockcroft-Gault: ClCr = ((140-idade) * peso) / (72 * creat) (* 0.85 se mulher)
    clcr = ((140 - idade) * peso) / (72 * creat)
    if sexo == "Feminino": clcr *= 0.85
    return round(clcr, 2)

def show():
    st.markdown("### 🛠️ Arsenal do Interno | Padrão Ouro")
    
    aba1, aba2, aba3 = st.tabs(["🧮 Calculadoras", "🫀 Semiótica", "📝 Auditor de Evolução"])

    with aba1:
        st.subheader("Ajuste de Dose e Função Renal")
        col1, col2 = st.columns(2)
        with col1:
            peso = st.number_input("Peso (kg)", value=70.0)
            idade = st.number_input("Idade", value=60)
        with col2:
            creat = st.number_input("Creatinina (mg/dL)", value=1.0)
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
        
        clcr = calculadora_renal(peso, idade, creat, sexo)
        st.metric("Clearance de Creatinina", f"{clcr} mL/min")
        
        medicamento = st.text_input("Medicamento para conferir ajuste:", placeholder="Ex: Enoxaparina, Vancomicina...")
        if st.button("Consultar Ajuste ⚡"):
            with st.spinner("IA consultando diretrizes de ajuste renal..."):
                prompt = f"Paciente com ClCr de {clcr} mL/min. Qual o ajuste de dose para {medicamento} segundo as diretrizes atuais?"
                resp, _ = consultar_core_ia_avancado(prompt)
                st.info(resp)

    with aba2:
        st.subheader("Guia de Exame Físico Cardiovascular")
        achado = st.text_area("Descreva o sopro ou achado (ex: Sopro sistólico em foco aórtico, irradia para carótida):")
        if st.button("Analisar Semiótica 🔍"):
            prompt = f"Análise semiótica: {achado}. Sugira hipóteses diagnósticas e manobras dinâmicas para confirmação."
            resp, _ = consultar_core_ia_avancado(prompt)
            st.success(resp)
        

    with aba3:
        st.subheader("Auditoria de Evolução Clínica")
        st.caption("Cole sua evolução para que a IA verifique se faltou algum dado vital.")
        evolucao = st.text_area("Texto da sua evolução:", height=200)
        if st.button("Auditar 🛡️"):
            prompt = f"Aja como um preceptor ranzinza. Critique esta evolução médica de internato e aponte o que faltou ou está impreciso: {evolucao}"
            resp, _ = consultar_core_ia_avancado(prompt)
            st.warning(resp)
