import streamlit as st
from groq import Groq
import json
import io
import re
import PyPDF2
import docx
import pptx
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from database import salvar_item_estudo

def get_ai_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def consultar_core_ia_perfeicao(prompt, contexto="", img_b64=None):
    client = get_ai_client()
    sys_msg = "Você é o CORE NEXUS, um Médico Preceptor de elite. Responda de forma clínica, estruturada (use bullet points e negritos) e baseada em evidências."
    full_prompt = f"Contexto do Arquivo:\n{contexto}\n\nComando do Usuário:\n{prompt}"
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": full_prompt}],
        temperature=0.3
    )
    res = completion.choices[0].message.content
    return res, "Geral", "Clínica"

def limpar_json(texto):
    texto = texto.strip()
    marca_json = "```" + "json"
    marca_simples = "```"
    if texto.startswith(marca_json): texto = texto[7:]
    elif texto.startswith(marca_simples): texto = texto[3:]
    if texto.endswith(marca_simples): texto = texto[:-3]
    return texto.strip()

def gerar_apenas_flashcards(texto_base, area, subtema, email, qtd=5):
    client = get_ai_client()
    prompt = (
        f"Baseado no texto, crie {qtd} Flashcards diretos.\n"
        "Retorne EXCLUSIVAMENTE um objeto JSON puro. Nao use crases.\n"
        "Formato: { \"flashcards\": [ { \"pergunta\": \"...\", \"resposta\": \"...\" } ] }\n"
        f"Texto: {texto_base}"
    )
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        cards = json.loads(limpar_json(completion.choices[0].message.content))
        lista = cards.get("flashcards", cards) if isinstance(cards, dict) else cards
        count = 0
        if isinstance(lista, list):
            for c in lista:
                if isinstance(c, dict) and "pergunta" in c and "resposta" in c:
                    salvar_item_estudo({"pergunta": c["pergunta"], "resposta": c["resposta"], "grande_area": area, "subtema": subtema, "categoria": "Flashcard", "criado_por_email": email})
                    count += 1
        return count
    except: return 0

def gerar_apenas_questoes(texto_base, area, subtema, email, qtd=3):
    client = get_ai_client()
    prompt = (
        f"Crie {qtd} questoes de multipla escolha padrão residência.\n"
        "Retorne EXCLUSIVAMENTE um objeto JSON puro. Nao use crases.\n"
        "Formato: { \"questoes\": [ { \"pergunta\": \"...\", \"a\": \"...\", \"b\": \"...\", \"c\": \"...\", \"d\": \"...\", \"gabarito\": \"A\", \"explicacao\": \"...\" } ] }\n"
        f"Texto: {texto_base}"
    )
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        dados = json.loads(limpar_json(completion.choices[0].message.content))
        questoes = dados.get("questoes", dados) if isinstance(dados, dict) else dados
        count = 0
        if isinstance(questoes, list):
            from database import get_supabase
            for q in questoes:
                if isinstance(q, dict):
                    get_supabase().table("questionarios").insert({"pergunta": q.get("pergunta", ""), "opcao_a": q.get("a", ""), "opcao_b": q.get("b", ""), "opcao_c": q.get("c", ""), "opcao_d": q.get("d", ""), "gabarito": q.get("gabarito", "A"), "explica_correta": q.get("explicacao", ""), "criado_por_email": email}).execute()
                    count += 1
        return count
    except: return 0

def ler_documento_universal(arquivo):
    if arquivo is None: return ""
    nome = arquivo.name.lower()
    try:
        texto_puro = ""
        if nome.endswith(".txt"): 
            texto_puro = arquivo.getvalue().decode("utf-8", errors="ignore")
        elif nome.endswith(".pdf"):
            pdf = PyPDF2.PdfReader(arquivo)
            texto_puro = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif nome.endswith(".docx"):
            doc = docx.Document(arquivo)
            texto_puro = " ".join([p.text for p in doc.paragraphs])
        elif nome.endswith(".pptx"):
            ppt = pptx.Presentation(arquivo)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"): texto_puro += shape.text + " "
        
        # Limpeza agressiva de texto para não confundir a IA (Remove quebras de linha quebradas do PDF)
        texto_limpo = re.sub(r'\s+', ' ', texto_puro)
        return texto_limpo
    except Exception as e: return f"Erro ao ler arquivo: {e}"

def gerar_pdf_premium(texto, titulo="Protocolo Nexus"):
    buffer = io.BytesIO()
    # Usando Platypus para design de nível superior
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, spaceAfter=20, textColor='#1e293b')
    sub_style = ParagraphStyle('SubStyle', parent=styles['Heading2'], fontSize=12, spaceAfter=15, textColor='#3b82f6')
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=11, spaceAfter=10, leading=16)
    
    story = []
    story.append(Paragraph("<b>CORE NEXUS | Inteligência Médica</b>", title_style))
    story.append(Paragraph(f"<i>{titulo}</i>", sub_style))
    story.append(Spacer(1, 15))
    
    # Conversão básica de Markdown para tags HTML do ReportLab
    texto_formatado = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto) # Negrito
    texto_formatado = re.sub(r'\*(.*?)\*', r'<i>\1</i>', texto_formatado) # Itálico
    
    for paragrafo in texto_formatado.split('\n'):
        if paragrafo.strip():
            story.append(Paragraph(paragrafo.strip(), normal_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()