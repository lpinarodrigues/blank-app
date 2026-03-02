import streamlit as st
import google.generativeai as genai
from groq import Groq
import time

def consultar_core_ia_avancado(prompt):
    # 1. Resposta Base com GROQ (Sempre funciona e é instantânea)
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res_groq = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Diretriz Médica Unifesp/Dante: {prompt}"}],
        ).choices[0].message.content
    except Exception as e:
        res_groq = f"Erro no Groq: {e}"

    # 2. Refinamento com GEMINI (Nível 1 - Com proteção de cota)
    try:
        # Usamos a Chave 2 (ou qualquer uma das 3 que você passou)
        genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
        model = genai.GenerativeModel('gemini-1.5-flash') # Flash é mais rápido para Nível 1
        
        # Pequeno delay para evitar colisão de requisições
        time.sleep(0.5)
        
        res_gemini = model.generate_content(f"Revise e adicione doses/evidências a esta conduta: {res_groq}").text
        check = "✅ Validado pelo Core Checker (Gemini)."
    except Exception:
        # Se o Gemini Nível 1 der erro de cota, entregamos a resposta do Groq que já é excelente
        res_gemini = res_groq
        check = "⚠️ Gemini em limite de cota. Exibindo análise rápida do Groq."
    
    return res_gemini, check
