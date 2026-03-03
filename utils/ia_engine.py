import streamlit as st
import google.generativeai as genai
import json

def processar_arquivo_para_estudo(conteudo_arquivo, email):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Aja como um examinador de prova de Título de Especialista.
    Com base no arquivo fornecido, gere 5 questões de múltipla escolha (A-D) de ALTÍSSIMO NÍVEL.
    
    PARA CADA QUESTÃO, você DEVE fornecer:
    1. A resposta correta com justificativa.
    2. JUSTIFICATIVA PARA CADA DISTRATOR (Por que a B está errada? Por que a C está errada?).
    3. 'Área de Reforço': O que o aluno deve estudar se errou essa alternativa específica.
    
    Retorne em JSON:
    [{{
        "pergunta": "", "opcao_a": "", "opcao_b": "", "opcao_c": "", "opcao_d": "",
        "gabarito": "A",
        "justificativa_correta": "",
        "comentario_distratores": {{"A": "", "B": "", "C": "", "D": ""}},
        "area_reforco": ""
    }}]
    """
    res = model.generate_content([prompt, conteudo_arquivo]).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return []
