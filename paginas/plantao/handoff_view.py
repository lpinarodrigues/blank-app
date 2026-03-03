import streamlit as st
import google.generativeai as genai
import json
from database import salvar_handoff, listar_ultimos_handoffs
from utils.pdf_generator import gerar_pdf_sbar

def processar_sbar_ia(texto):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Aja como um preceptor de UTI. Transforme este relato clínico no formato SBAR (Situation, Background, Assessment, Recommendation).
    Identifique também possíveis RED FLAGS (riscos iminentes).
    Texto: {texto}
    Retorne apenas JSON: {{"situation": "", "background": "", "assessment": "", "recommendation": "", "red_flags": ""}}
    """
    res = model.generate_content(prompt).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return None

def show():
    st.markdown("### 🚑 Passagem de Plantão | SBAR & Safety")
    email = st.session_state.get('user_email', 'lucas.pina@unifesp.br')
    
    with st.expander("📝 Nova Passagem (Handoff)", expanded=True):
        leito = st.text_input("Leito/Iniciais do Paciente:")
        relato = st.text_area("Relato Clínico:", height=150)
        
        if st.button("Gerar e Validar ⚡"):
            with st.spinner("IA estruturando..."):
                sbar = processar_sbar_ia(relato)
                if sbar:
                    salvar_handoff(email, leito, relato, sbar, sbar['red_flags'])
                    st.session_state['ultimo_sbar'] = {"paciente_leito": leito, "sbar_json": sbar, "red_flags": sbar['red_flags'], "created_at": "Agora"}
                    st.success("Handoff salvo!")

    if 'ultimo_sbar' in st.session_state:
        pdf = gerar_pdf_sbar(st.session_state['ultimo_sbar'])
        st.download_button(
            label="📄 Baixar PDF do Plantão",
            data=pdf,
            file_name=f"handoff_{st.session_state['ultimo_sbar']['paciente_leito']}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.divider()
    st.subheader("📋 Histórico Recente")
    for h in listar_ultimos_handoffs():
        with st.container(border=True):
            st.markdown(f"**Leito {h['paciente_leito']}**")
            st.caption(f"Status: {h['sbar_json'].get('situation')}")
