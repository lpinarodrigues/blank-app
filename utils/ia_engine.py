import streamlit as st
import google.generativeai as genai
import json

def gerar_conteudo_hierarquico(tema_base):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Gere 5 itens de estudo sobre {tema_base}.
    Classifique OBRIGATORIAMENTE em:
    - grande_area: (Clínica Médica, Cirurgia, etc)
    - subtema: (Cardiologia, Gastro, etc)
    - tema_especifico: (Apendicite, IAM, etc)
    - complexidade: (1-3)
    
    Retorne JSON:
    [{{
        "pergunta": "", "resposta": "", "grande_area": "", 
        "subtema": "", "tema_especifico": "", "complexidade": 2,
        "justificativa": ""
    }}]
    """
    res = model.generate_content(prompt).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return []
