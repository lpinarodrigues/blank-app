import streamlit as st
import google.generativeai as genai
import json

def configurar_gemini():
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    return genai.GenerativeModel('gemini-1.5-pro')

def dissecar_arquivo_master(conteudo, area, subtema):
    model = configurar_gemini()
    prompt = f"""
    Aja como examinador do TEC (SBC). Baseado no texto, gere 10 questões A-D.
    Hierarquia: Área: {area} | Subtema: {subtema}.
    
    PARA CADA QUESTÃO:
    - Justificativa detalhada da CORRETA.
    - JUSTIFICATIVA DE CADA ERRO (Distratores A, B, C, D).
    - Dica de 'Área de Reforço'.
    
    RETORNE APENAS JSON:
    [{{
        "pergunta": "", "a": "", "b": "", "c": "", "d": "", "gabarito": "A",
        "explica_correta": "", "explica_erros": {{"A":"","B":"","C":"","D":""}},
        "reforco": ""
    }}]
    """
    res = model.generate_content([prompt, conteudo]).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return []
