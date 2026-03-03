import streamlit as st
import google.generativeai as genai
from groq import Groq
import json
import random

def configurar_gemini():
    # Pool de chaves para evitar limites de quota (Rotation)
    chaves = [
        st.secrets["GEMINI_CHAVE_1"],
        st.secrets["GEMINI_CHAVE_2"],
        st.secrets["GEMINI_CHAVE_3"]
    ]
    genai.configure(api_key=random.choice(chaves))
    return genai.GenerativeModel('gemini-1.5-pro')

def consultar_core_ia_perfeicao(prompt, modo="Beira de Leito"):
    """Motor Principal via Groq (Llama 3.3 70B) - Ultra Rápido"""
    instrucao = f"Aja como Preceptor Sênior da Unifesp/Dante. Modo: {modo}. Foco em diretrizes 2024-2026."
    
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": instrucao},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content, "⚡ Powered by GROQ (Llama 3.3)"
    except Exception as e:
        # Fallback Automático para Gemini se a Groq falhar
        model = configurar_gemini()
        res = model.generate_content(f"{instrucao}\n\n{prompt}").text
        return res, "🛡️ Fallback: Gemini 1.5 Pro"

def gerar_batch_flashcards(texto, tema, email):
    """Geração Massiva de Conteúdo usando Gemini (Melhor para Contextos Longos)"""
    model = configurar_gemini()
    p = f"Gere 15 flashcards nível residência sobre {tema}. Retorne estritamente JSON: [{{'p': '', 'r': '', 'area': '', 'subtema': ''}}]"
    try:
        res = model.generate_content([p, texto]).text
        cards = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_item_estudo
        for c in cards:
            c['criado_por_email'] = email
            c['is_global'] = True
            c['grande_area'] = c.get('area', 'Clínica Médica')
            c['subtema'] = c.get('subtema', tema)
            salvar_item_estudo(c)
        return len(cards)
    except:
        return 0
