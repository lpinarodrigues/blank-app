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
    Aja como Preceptor Sênior. Crie um material EXTENSO e DETALHADO.
    Estrutura:
    1. 💊 Conduta Imediata
    2. 📈 Escores
    3. 🩺 Caso Clínico Simulado
    4. ⚠️ Red Flags
    5. 📚 Referências REAIS (Formato VANCOUVER Estrito com DOI/Páginas).
    
    Adicione OBRIGATORIAMENTE no final esta exata linha:
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

def extrair_json_seguro(texto):
    try:
        match = re.search(r'\[\s*\{.*?\}\s*\]', texto, re.DOTALL)
        if match: return json.loads(match.group(0))
        return json.loads(texto)
    except: return []

def gerar_apenas_flashcards(texto, area, subtema, email):
    model = configurar_gemini()
    p = f"Gere 5 flashcards avançados. JSON: [{{\"p\": \"pergunta\", \"r\": \"resposta\"}}]. Texto: {texto}"
    try:
        res = extrair_json_seguro(model.generate_content(p).text)
        from database import salvar_item_estudo
        count = 0
        for f in res:
            if salvar_item_estudo({"pergunta": f['p'], "resposta": f['r'], "grande_area": area, "subtema": subtema, "categoria": "Flashcard", "is_global": True, "criado_por_email": email}): count+=1
        return count
    except: return 0

def gerar_apenas_questoes(texto, area, subtema, email):
    model = configurar_gemini()
    p = f"Gere 3 questões ABCD. JSON: [{{\"pergunta\": \"\", \"a\": \"\", \"b\": \"\", \"c\": \"\", \"d\": \"\", \"gabarito\": \"A\", \"justificativa\": \"\"}}]. Texto: {texto}"
    try:
        res = extrair_json_seguro(model.generate_content(p).text)
        from database import salvar_questao
        count = 0
        for q in res:
            if salvar_questao({"pergunta": q['pergunta'], "opcao_a": q['a'], "opcao_b": q['b'], "opcao_c": q['c'], "opcao_d": q['d'], "gabarito": q['gabarito'], "explica_correta": q['justificativa'], "grande_area": area, "subtema": subtema, "is_global": True}): count+=1
        return count
    except: return 0

def add_discreet_tracking(canvas, doc, email):
    """Metadados e Rastreio Invisível (Base64) disfarçado de código de sistema"""
    canvas.saveState()
    # 1. Rastreio visual minúsculo no rodapé (Parece um número de série de sistema)
    codigo_rastreio = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    canvas.setFont('Helvetica', 6)
    canvas.setFillGray(0.7) # Cinza bem claro
    canvas.drawString(30, 20, f"Ref: CNX-{codigo_rastreio[:15]}... | SysDoc")
    canvas.restoreState()

def gerar_pdf_resposta(texto, email):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    # 2. Metadados do Arquivo (Rastreio Digital)
    doc.title = "Protocolo CORE NEXUS"
    doc.author = email 
    doc.subject = f"Gerado em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Normal_Justify', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=12, fontSize=11, leading=16)
    
    # Cabeçalho Premium CORE NEXUS
    header_data = [[Paragraph("<font color='white' size='16'><b>CORE NEXUS</b></font> <br/><font color='#A9Cce3'>Terminal Médico de Elite</font>"), ""]]
    t = Table(header_data, colWidths=[400, 100])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0B2D5C')), ('PADDING', (0,0), (-1,-1), 12)]))
    
    story = [t, Spacer(1, 20)]
    
    # Renderizar Markdown (Negritos) para o PDF
    texto_formatado = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto) # Converte **negrito** para <b>negrito</b>
    texto_formatado = texto_formatado.replace('💊', '').replace('🩺', '').replace('⚠️', '').replace('📈', '').replace('📚', '')
    
    for paragrafo in texto_formatado.split('\n\n'):
        if paragrafo.strip():
            story.append(Paragraph(paragrafo.replace('\n', '<br/>'), style_normal))
            
    doc.build(story, onFirstPage=lambda c, d: add_discreet_tracking(c, d, email), onLaterPages=lambda c, d: add_discreet_tracking(c, d, email))
    
    buffer.seek(0)
    return buffer
