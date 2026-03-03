import streamlit as st
import google.generativeai as genai
import json
import re
import base64
from io import BytesIO
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors

def configurar_gemini():
    chaves = ["GEMINI_CHAVE_1", "GEMINI_CHAVE_2", "GEMINI_CHAVE_3"]
    for k in chaves:
        if k in st.secrets:
            try:
                genai.configure(api_key=st.secrets[k])
                return genai.GenerativeModel('gemini-1.5-pro')
            except: continue
    return None

def consultar_core_ia_perfeicao(prompt):
    instrucao = """
    Aja como Preceptor Sênior de um hospital de referência. Crie um material EXTENSO, PROFUNDO e EXTREMAMENTE DETALHADO.
    
    Estrutura OBRIGATÓRIA:
    1. 💊 Conduta Imediata e Fisiopatologia (Doses, vias, mecanismos).
    2. 🌍 Diretrizes Comparadas (Compare Brasil, EUA e Europa. Cite as diferenças de conduta, se houver).
    3. 🩺 Sinais Clínicos (Destaque os "Clássicos" e os "Frequentemente Ignorados" no PS).
    4. ⚖️ Diagnóstico Diferencial (Quais doenças mais se confundem com ela e como "matar a charada").
    5. 📈 Escores e Critérios Diagnósticos.
    6. ⚠️ Red Flags e Complicações.
    7. 📚 Referências REAIS (ESTRITAMENTE PADRÃO VANCOUVER). 
       - REGRAS DE REFERÊNCIA: Máximo de 8 anos de publicação (exceto diretrizes clássicas intocáveis). Inclua DOI, Volume e Páginas reais.
    
    Adicione OBRIGATORIAMENTE no final esta exata linha para o sistema classificar o resumo:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    """
    
    try:
        from groq import Groq
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt}],
            temperature=0.3
        ).choices[0].message.content
        
        area, subtema = "Clínica Médica", "Geral"
        if "TAGS_GERADAS:" in res:
            partes = res.split("TAGS_GERADAS:")
            texto_principal = partes[0].strip()
            tags = partes[1].split("|")
            area = tags[0].strip() if len(tags) > 0 else "Geral"
            subtema = tags[1].strip() if len(tags) > 1 else "Geral"
        else:
            texto_principal = res
        return texto_principal, area, subtema
    except Exception as e: return f"Erro: {e}", "Erro", "Erro"

# [RESTANTE DAS FUNÇÕES (Flashcards, Questoes, PDF) MANTIDAS IGUAIS AO SCRIPT ANTERIOR]
# Para encurtar, assuma que extrair_json_seguro, gerar_apenas_flashcards, gerar_apenas_questoes, 
# add_discreet_tracking e gerar_pdf_resposta continuam exatamente iguais ao código anterior, perfeitos.
