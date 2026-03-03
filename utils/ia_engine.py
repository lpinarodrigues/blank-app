import streamlit as st
import google.generativeai as genai
import json
import random
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def configurar_gemini():
    chaves = ["GEMINI_CHAVE_1", "GEMINI_CHAVE_2", "GEMINI_CHAVE_3"]
    for k in chaves:
        if k in st.secrets:
            try:
                genai.configure(api_key=st.secrets[k])
                return genai.GenerativeModel('gemini-1.5-pro')
            except: continue
    return None

def consultar_core_ia_perfeicao(prompt, modo="Beira de Leito"):
    model = configurar_gemini()
    instrucao = f"""
    Aja como um Preceptor Médico de Excelência. Modo: {modo}.
    Estrutura: 1. Conduta | 2. Escores | 3. Caso Clínico | 4. Red Flags.
    
    REFERÊNCIAS: No final, liste 3 referências REAIS em formato VANCOUVER.
    Verifique a veracidade (Autores, Título, Revista, Ano).
    
    AUTO-RESUMO: Gere um resumo técnico de 3 linhas para a área de estudos.
    """
    if model:
        res = model.generate_content(f"{instrucao}\n\nPergunta: {prompt}").text
        # Separar Referências e Resumo (Lógica de Parsing Simples)
        return res, "💎 Resposta Estruturada"
    return "Erro de configuração.", "❌ Erro"

def gerar_pdf_resposta(texto):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "CORE NEXUS - Relatório de Conduta")
    p.setFont("Helvetica", 10)
    
    textobject = p.beginText(100, 730)
    for line in texto.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
