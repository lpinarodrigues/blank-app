import streamlit as st
import google.generativeai as genai
import json
from database import salvar_handoff, listar_ultimos_handoffs

def processar_sbar_ia(texto):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Aja como um preceptor de UTI. Transforme este relato clínico no formato SBAR (Situation, Background, Assessment, Recommendation).
    Identifique também possíveis RED FLAGS (riscos iminentes).
    Texto: {texto}
    Retorne em JSON: {{"situation": "", "background": "", "assessment": "", "recommendation": "", "red_flags": ""}}
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
        relato = st.text_area("Relato Clínico (Dite ou Escreva):", height=150, placeholder="Ex: Paciente no 402B, pós-operatório de troca valvar, evoluindo com hipotensão...")
        
        if st.button("Gerar SBAR e Validar ⚡"):
            with st.spinner("IA estruturando passagem segura..."):
                sbar = processar_sbar_ia(relato)
                if sbar:
                    st.success("Estrutura SBAR Gerada!")
                    st.json(sbar)
                    salvar_handoff(email, leito, relato, sbar, sbar['red_flags'])
                    if sbar['red_flags']:
                        st.error(f"🚨 RED FLAG: {sbar['red_flags']}")
    
    st.divider()
    st.subheader("📋 Últimos Handoffs da Equipe")
    historico = listar_ultimos_handoffs()
    for h in historico:
        with st.container(border=True):
            st.caption(f"Leito: {h['paciente_leito']} | Por: {h['medico_email']}")
            st.markdown(f"**Recomendação:** {h['sbar_json'].get('recommendation', '')}")
