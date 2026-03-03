import streamlit as st
import google.generativeai as genai
import random
import json

def configurar_gemini():
    # Tenta usar as chaves em ordem, se uma falhar, tenta a próxima
    chaves = ["GEMINI_CHAVE_1", "GEMINI_CHAVE_2", "GEMINI_CHAVE_3"]
    for k in chaves:
        if k in st.secrets:
            try:
                genai.configure(api_key=st.secrets[k])
                model = genai.GenerativeModel('gemini-1.5-pro')
                # Teste rápido de conexão
                return model
            except:
                continue
    return None

def consultar_core_ia_perfeicao(prompt, modo="Beira de Leito"):
    # Prioridade para GROQ (Velocidade de Preceptor)
    if "GROQ_API_KEY" in st.secrets:
        try:
            from groq import Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content
            return res, "⚡ Groq Performance"
        except:
            pass
            
    # Fallback para Gemini se Groq falhar ou não existir
    model = configurar_gemini()
    if model:
        res = model.generate_content(prompt).text
        return res, "🛡️ Gemini Fallback"
    return "Erro: Configure as chaves nos Secrets do Streamlit.", "❌ Erro"
