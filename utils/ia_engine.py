import streamlit as st
import google.generativeai as genai
import json

def gerar_cards_cloze(tema):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Aja como um designer de questões do USMLE Step 2.
    Gere 5 flashcards de 'Cloze Deletion' sobre {tema}.
    O Cloze Deletion deve ocultar a informação MAIS importante entre colchetes [...].
    
    Exemplo: "A tríade de Beck consiste em hipofonese de bulhas, turgência jugular e [...]" -> "hipotensão".
    
    Retorne apenas JSON: [{{"texto_omissao": "sentença com [...]", "resposta": "palavra oculta", "explicacao": "por que isso ocorre"}}]
    """
    res = model.generate_content(prompt).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return []
