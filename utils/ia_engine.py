import streamlit as st
import google.generativeai as genai
import json
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

def consultar_core_ia_perfeicao(prompt):
    model = configurar_gemini()
    instrucao = """
    Aja como Preceptor Sênior. Estrutura:
    1. 💊 Conduta Imediata
    2. 📈 Escores
    3. 🩺 Caso Clínico Simulado
    4. ⚠️ Red Flags
    5. 📚 Referências REAIS em formato VANCOUVER.
    
    No final da sua resposta, adicione OBRIGATORIAMENTE uma linha neste formato exato para o sistema classificar:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    Exemplo: TAGS_GERADAS: Clínica Médica | Cardiologia
    """
    if model:
        try:
            res = model.generate_content(f"{instrucao}\n\nPergunta: {prompt}").text
            area, subtema = "Geral", "Geral"
            if "TAGS_GERADAS:" in res:
                partes = res.split("TAGS_GERADAS:")
                texto_principal = partes[0].strip()
                tags = partes[1].split("|")
                if len(tags) >= 2:
                    area = tags[0].strip()
                    subtema = tags[1].strip()
            else:
                texto_principal = res
            return texto_principal, area, subtema
        except: return "Erro na IA.", "Geral", "Geral"
    return "Erro nas Chaves.", "Geral", "Geral"

def gerar_apenas_flashcards(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 3 flashcards médicos baseados no texto. Retorne apenas JSON: [{{'p': 'pergunta', 'r': 'resposta'}}]. Texto: {texto}"
    try:
        res = model.generate_content(prompt).text
        dados = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_item_estudo
        for f in dados:
            salvar_item_estudo({
                "pergunta": f['p'], "resposta": f['r'], "grande_area": area, 
                "subtema": subtema, "categoria": "Flashcard", "is_global": True, "criado_por_email": email
            })
        return dados
    except: return []

def gerar_apenas_questoes(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 2 questões de múltipla escolha (padrão residência) baseadas no texto. Retorne apenas JSON: [{{'pergunta': '', 'a': '', 'b': '', 'c': '', 'd': '', 'gabarito': 'A', 'justificativa': ''}}]. Texto: {texto}"
    try:
        res = model.generate_content(prompt).text
        dados = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_questao
        for q in dados:
            salvar_questao({
                "pergunta": q['pergunta'], "opcao_a": q['a'], "opcao_b": q['b'], 
                "opcao_c": q['c'], "opcao_d": q['d'], "gabarito": q['gabarito'], 
                "explica_correta": q['justificativa'], "grande_area": area, 
                "subtema": subtema, "is_global": True
            })
        return dados
    except: return []

def gerar_pdf_resposta(texto):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 750, "CORE NEXUS - Documento de Conduta")
    p.setFont("Helvetica", 10)
    textobject = p.beginText(50, 730)
    for line in texto.split('\n'):
        textobject.textLine(line[:110]) # Limita tamanho da linha
    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
