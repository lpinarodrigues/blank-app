import streamlit as st
import google.generativeai as genai
from groq import Groq
import json

def configurar_gemini():
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    return genai.GenerativeModel('gemini-1.5-pro')

def consultar_core_ia_perfeicao(prompt, modo="Beira de Leito"):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    instrucao = f"Aja como Preceptor Sênior da Unifesp/Dante. Modo: {modo}. Foco em diretrizes 2024-2026."
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt}],
    ).choices[0].message.content
    return res, "📚 Fontes: SBC, ESC, AHA, Sabiston."

def gerar_batch_flashcards(texto, tema, email):
    model = configurar_gemini()
    p = f"Gere 15 flashcards nível residência sobre {tema}. Retorne JSON: p, r, area, subtema."
    res = model.generate_content([p, texto]).text
    try:
        cards = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_item_estudo
        for c in cards:
            c['criado_por_email'] = email
            c['is_global'] = True # Salva na biblioteca geral
            salvar_item_estudo(c)
        return len(cards)
    except: return 0
