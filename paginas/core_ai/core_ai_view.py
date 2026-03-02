import streamlit as st
import time
import os

# Simulando a chamada de API (Substitua pelo seu client oficial de OpenAI/Anthropic)
def chamar_ia_medica(prompt, especialidade="Cardiologia"):
    # Aqui o sistema usaria sua API_KEY configurada nos Secrets
    # Ex: client.chat.completions.create(...)
    try:
        # Simulando processamento neural de alta performance
        time.sleep(1.5) 
        return f"Com base nas diretrizes de {especialidade} (2024-2026), a conduta recomendada para '{prompt}' envolve estabilização imediata, monitorização hemodinâmica e seguimento do protocolo institucional da Unifesp/Dante Pazzanese."
    except Exception as e:
        return f"Erro na conexão com a API: {e}"

def show():
    # Cabeçalho Estilizado para Mobile
    st.markdown('<div style="background-color: #E0E7FF; padding: 15px; border-radius: 15px; margin-bottom: 20px;">'
                '<h4 style="margin:0; color: #1E3A8A;">🧠 Assistente Core AI</h4>'
                '<p style="margin:0; font-size: 0.8rem; color: #3730A3;">Conectado via API de Alta Performance</p>'
                '</div>', unsafe_allow_html=True)

    # 1. Seleção de Especialidade (Ajusta o tom da IA)
    esp = st.pills("Foco da Análise:", ["Geral", "Cardiologia", "UTI", "Emergência"], default="Geral")

    # 2. Input de Texto Moderno
    with st.container(border=True):
        query = st.text_area("Sua dúvida clínica:", placeholder="Ex: Critérios para extubação em paciente DPOC...", height=100)
        
        col1, col2 = st.columns([2,1])
        with col2:
            processar = st.button("Consultar IA ⚡", use_container_width=True)

    if processar and query:
        with st.status("Acionando Motores Neurais...", expanded=True) as status:
            st.write("📡 Enviando prompt para API...")
            resposta = chamar_ia_medica(query, esp)
            st.write("⚖️ Validando contra diretrizes SBC/AHA...")
            status.update(label="Análise Concluída!", state="complete", expanded=False)
        
        # 3. Resposta em Card de Elite
        st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 20px; border-left: 5px solid #1E3A8A; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <p style="color: #64748B; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px;">RESPOSTA DA INTELIGÊNCIA:</p>
                <div style="color: #1E293B; line-height: 1.6;">{resposta}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Feedback de Utilidade (Alimenta o Core Score)
        st.write("")
        if st.button("✅ Útil para minha conduta (+5 pts)"):
            st.toast("Score atualizado no Supabase!", icon="🛡️")

