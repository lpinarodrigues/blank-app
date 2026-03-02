import streamlit as st
import google.generativeai as genai
from groq import Groq

def agente_sentinela(contexto):
    # Usa a Chave 1 para monitorar o status do sistema
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_1"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content(f"Verifique a consistência deste estado do app: {contexto}").text

def consultar_core_ia_avancado(prompt):
    # Passo 1: Resposta Ultra-Rápida com Groq
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    res_groq = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    ).choices[0].message.content

    # Passo 2: Refinamento com Gemini Chave 2
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    model_refine = genai.GenerativeModel('gemini-1.5-pro')
    res_gemini = model_refine.generate_content(f"Refine esta conduta médica: {res_groq}").text

    # Passo 3: Checagem de Erros com Gemini Chave 3
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_3"])
    model_check = genai.GenerativeModel('gemini-1.5-flash')
    checagem = model_check.generate_content(f"Há algum erro de diretriz nesta resposta? {res_gemini}").text
    
    return res_gemini, checagem
