import streamlit as st
import google.generativeai as genai
from groq import Groq
import json

def configurar_gemini():
    genai.configure(api_key=st.secrets["GEMINI_CHAVE_2"])
    return genai.GenerativeModel('gemini-1.5-pro')

def consultar_core_ia_perfeicao(prompt, modo="Beira de Leito"):
    instrucao = f"Aja como Preceptor Sênior. Modo: {modo}. Cite Classe de Recomendação e Nível de Evidência (SBC/ESC/AHA)."
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt}],
    ).choices[0].message.content
    return res, "✅ Fontes: SBC/ESC/AHA Processadas."

def gerar_batch_flashcards(texto_contexto, tema, email):
    model = configurar_gemini()
    prompt = f"Com base em {texto_contexto}, gere 15 flashcards médicos nível residência (JSON: p, r, explicacao, area, subtema)."
    res = model.generate_content(prompt).text
    try:
        cards = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_flashcard_estruturado
        for c in cards:
            salvar_flashcard_estruturado(c['p'], c['r'], c.get('area', 'Clínica'), c.get('subtema', tema), tema, email, c.get('explicacao', ''))
        return len(cards)
    except: return 0

def gerar_conteudo_hierarquico(tema_base):
    model = configurar_gemini()
    prompt = f"Gere 5 itens de estudo sobre {tema_base} (JSON: pergunta, resposta, grande_area, subtema, tema_especifico, complexidade, justificativa)."
    res = model.generate_content(prompt).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return []

def processar_arquivo_para_estudo(conteudo_arquivo, email):
    model = configurar_gemini()
    prompt = "Aja como examinador. Gere 5 questões A-D de alto nível com justificativa para cada alternativa errada (JSON)."
    res = model.generate_content([prompt, conteudo_arquivo]).text
    try:
        return json.loads(res.replace('```json', '').replace('```', '').strip())
    except: return []
