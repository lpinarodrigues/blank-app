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
    4. ⚖️ Diagnóstico Diferencial (Quais doenças mais se confundem com ela e como fazer o diagnóstico diferencial).
    5. 📈 Escores e Critérios Diagnósticos.
    6. ⚠️ Red Flags e Complicações.
    7. 📚 Referências REAIS (ESTRITAMENTE PADRÃO VANCOUVER). 
       - REGRAS DE REFERÊNCIA: Máximo de 8 anos de publicação (exceto diretrizes clássicas). Inclua DOI, Volume e Páginas reais.
    
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

# --- FUNÇÕES QUE FALTARAM E CAUSAVAM O ERRO ---
def gerar_apenas_flashcards(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 5 flashcards avançados sobre o texto. Retorne APENAS o JSON no formato exato: [{{\"p\": \"pergunta\", \"r\": \"resposta\"}}]. Sem texto adicional. Texto: {texto}"
    try:
        res = model.generate_content(prompt).text
        dados = extrair_json_seguro(res)
        from database import salvar_item_estudo
        count = 0
        for f in dados:
            if salvar_item_estudo({"pergunta": f['p'], "resposta": f['r'], "grande_area": area, "subtema": subtema, "categoria": "Flashcard", "is_global": True, "criado_por_email": email}): count+=1
        return count
    except: return 0

def gerar_apenas_questoes(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 3 questões de residência ABCD. Retorne APENAS o JSON no formato: [{{\"pergunta\": \"\", \"a\": \"\", \"b\": \"\", \"c\": \"\", \"d\": \"\", \"gabarito\": \"A\", \"justificativa\": \"\"}}]. Texto: {texto}"
    try:
        res = model.generate_content(prompt).text
        dados = extrair_json_seguro(res)
        from database import salvar_questao
        count = 0
        for q in dados:
            if salvar_questao({"pergunta": q['pergunta'], "opcao_a": q['a'], "opcao_b": q['b'], "opcao_c": q['c'], "opcao_d": q['d'], "gabarito": q['gabarito'], "explica_correta": q['justificativa'], "grande_area": area, "subtema": subtema, "is_global": True}): count+=1
        return count
    except: return 0

def add_discreet_tracking(canvas, doc, email):
    canvas.saveState()
    codigo_rastreio = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    canvas.setFont('Helvetica', 6)
    canvas.setFillGray(0.7)
    canvas.drawString(30, 20, f"Ref: CNX-{codigo_rastreio[:15]}... | SysDoc")
    canvas.restoreState()

def gerar_pdf_resposta(texto, email):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    doc.title = "Protocolo CORE NEXUS"
    doc.author = email 
    doc.subject = f"Gerado em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Normal_Justify', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=12, fontSize=11, leading=16)
    
    header_data = [[Paragraph("<font color='white' size='16'><b>CORE NEXUS</b></font> <br/><font color='#A9Cce3'>Terminal Médico de Elite</font>"), ""]]
    t = Table(header_data, colWidths=[400, 100])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0B2D5C')), ('PADDING', (0,0), (-1,-1), 12)]))
    
    story = [t, Spacer(1, 20)]
    
    texto_formatado = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    texto_formatado = texto_formatado.replace('💊', '').replace('🩺', '').replace('⚠️', '').replace('📈', '').replace('📚', '').replace('🌍', '').replace('⚖️', '')
    
    for paragrafo in texto_formatado.split('\n\n'):
        if paragrafo.strip():
            story.append(Paragraph(paragrafo.replace('\n', '<br/>'), style_normal))
            
    doc.build(story, onFirstPage=lambda c, d: add_discreet_tracking(c, d, email), onLaterPages=lambda c, d: add_discreet_tracking(c, d, email))
    
    buffer.seek(0)
    return buffer
