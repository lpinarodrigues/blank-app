import streamlit as st
import google.generativeai as genai
import json

def gerar_questao_medica_ia(tema, dificuldade="Média"):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Aja como um preceptor de Cardiologia do Dante Pazzanese. 
    Gere uma questão de múltipla escolha no padrão da prova de Título SBC (TEC) sobre: {tema}.
    Nível de dificuldade: {dificuldade}.
    
    Retorne EXATAMENTE no formato JSON abaixo, sem textos adicionais:
    {{
        "pergunta": "texto da pergunta",
        "opcao_a": "texto a",
        "opcao_b": "texto b",
        "opcao_c": "texto c",
        "opcao_d": "texto d",
        "gabarito": "A, B, C ou D",
        "comentario_ia": "explicação técnica breve",
        "referencia": "Diretriz SBC 2024",
        "categoria": "{tema}",
        "dificuldade": "{dificuldade}"
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        # Limpa possíveis markdown do json
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except:
        return None
