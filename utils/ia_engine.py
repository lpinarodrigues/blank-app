import streamlit as st
import google.generativeai as genai
import json
from database import salvar_flashcard

def gerar_batch_flashcards(texto_contexto, tema, email):
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Com base no contexto médico abaixo, gere 15 flashcards de ALTO NÍVEL (padrão residência médica).
    Contexto: {texto_contexto}
    Tema: {tema}
    
    REGRAS:
    - Mescle perguntas diretas (P/R) e Cloze Deletion [...].
    - Foque em: Critérios diagnósticos, Doses de escolha, Complicações cirúrgicas e Condutas 'Red Flag'.
    - Formato JSON estrito: [{{"p": "pergunta", "r": "resposta", "explicacao": "base científica"}}]
    """
    
    try:
        res = model.generate_content(prompt).text
        cards = json.loads(res.replace('```json', '').replace('```', '').strip())
        for c in cards:
            salvar_flashcard(c['p'], c['r'], tema, email, c['explicacao'])
        return len(cards)
    except:
        return 0
