import streamlit as st
import google.generativeai as genai
import json
import re
import base64
from io import BytesIO
import datetime
import PyPDF2
import docx
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
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

def ler_arquivo_texto(arquivo_upload):
    """Extrai texto de PDFs, DOCX e TXT"""
    try:
        if arquivo_upload.name.endswith('.pdf'):
            leitor = PyPDF2.PdfReader(arquivo_upload)
            return " ".join([p.extract_text() for p in leitor.pages if p.extract_text()])
        elif arquivo_upload.name.endswith('.docx'):
            doc = docx.Document(arquivo_upload)
            return " ".join([p.text for p in doc.paragraphs])
        else:
            return arquivo_upload.getvalue().decode('utf-8')
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"

def consultar_core_ia_perfeicao(prompt, texto_contexto=""):
    contexto_adicional = f"\n\nBASEIE-SE TAMBÉM NESTE DOCUMENTO FORNECIDO PELO USUÁRIO E CRUZE COM A LITERATURA ATUAL:\n{texto_contexto[:15000]}" if texto_contexto else ""
    
    instrucao = """
    Aja como Preceptor Titular de Harvard. LINGUAGEM ESTRITAMENTE TÉCNICA.
    Estrutura VISUAL OBRIGATÓRIA:
    1. 📌 FISIOPATOLOGIA E SUBTIPOS.
    2. 🔀 FLUXOGRAMA DE DECISÃO VISUAL (Use ➔).
    3. ⚖️ DIAGNÓSTICO DIFERENCIAL (Tabela de 3 colunas: Doença | Semelhança | Sinal Diferenciador/Patognomônico).
    4. 📈 ESCORES E CRITÉRIOS (Destrinche as variáveis).
    5. ⚠️ RED FLAGS.
    6. 📚 REFERÊNCIAS (Vancouver, máx 8 anos).
    
    Adicione OBRIGATORIAMENTE no final esta exata linha:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    """
    try:
        from groq import Groq
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt + contexto_adicional}],
            temperature=0.15
        ).choices[0].message.content
        
        area, subtema = "Clínica Médica", "Geral"
        if "TAGS_GERADAS:" in res:
            partes = res.split("TAGS_GERADAS:")
            texto_principal = partes[0].strip()
            tags = partes[1].split("|")
            area = tags[0].strip() if len(tags) > 0 else "Geral"
            subtema = tags[1].strip() if len(tags) > 1 else "Geral"
        else: texto_principal = res
        return texto_principal, area, subtema
    except Exception as e: return f"Erro: {e}", "Erro", "Erro"

def extrair_json_seguro(texto):
    """Filtro absoluto para evitar erros na conversão dos Flashcards/Questões"""
    texto = texto.replace('```json', '').replace('```', '')
    try:
        match = re.search(r'\[\s*\{.*?\}\s*\]', texto, re.DOTALL)
        if match: return json.loads(match.group(0))
        return json.loads(texto)
    except Exception as e:
        print(f"Erro JSON: {e}") # Log oculto
        return []

def gerar_apenas_flashcards(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 5 flashcards curtos. Retorne ESTRITAMENTE um Array JSON puro: [{{\"p\": \"pergunta\", \"r\": \"resposta\"}}]. Texto: {texto}"
    try:
        dados = extrair_json_seguro(model.generate_content(prompt).text)
        if not dados: return 0
        from database import salvar_item_estudo
        count = 0
        for f in dados:
            if salvar_item_estudo({"pergunta": f.get('p',''), "resposta": f.get('r',''), "grande_area": area, "subtema": subtema, "categoria": "Flashcard", "is_global": True, "criado_por_email": email}): count+=1
        return count
    except: return 0

def gerar_apenas_questoes(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 3 questões de residência ABCD. Retorne ESTRITAMENTE um Array JSON puro: [{{\"pergunta\": \"\", \"a\": \"\", \"b\": \"\", \"c\": \"\", \"d\": \"\", \"gabarito\": \"A\", \"justificativa\": \"\"}}]. Texto: {texto}"
    try:
        dados = extrair_json_seguro(model.generate_content(prompt).text)
        if not dados: return 0
        from database import salvar_questao
        count = 0
        for q in dados:
            if salvar_questao({"pergunta": q.get('pergunta',''), "opcao_a": q.get('a',''), "opcao_b": q.get('b',''), "opcao_c": q.get('c',''), "opcao_d": q.get('d',''), "gabarito": q.get('gabarito','A'), "explica_correta": q.get('justificativa',''), "grande_area": area, "subtema": subtema, "is_global": True}): count+=1
        return count
    except: return 0

def add_premium_header_footer(canvas, doc, email):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#0B2D5C'))
    canvas.rect(0, 740, 612, 52, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 18)
    canvas.drawString(40, 760, "CORE NEXUS")
    canvas.setFont('Helvetica', 10)
    canvas.drawString(40, 748, "Clinical Guidelines & Advanced Pathways")
    
    codigo_rastreio = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    canvas.setFont('Helvetica', 6)
    canvas.setFillGray(0.7)
    canvas.drawString(40, 20, f"ID: CNX-{codigo_rastreio[:15]} | Validated Document | {datetime.datetime.now().strftime('%Y-%m-%d')}")
    canvas.restoreState()

def gerar_pdf_resposta(texto, email):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=70, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Normal_Bullet', parent=styles['Normal'], textColor=colors.HexColor('#2C3E50'), alignment=TA_JUSTIFY, spaceAfter=10, fontSize=10, leading=15)
    style_h2 = ParagraphStyle('Heading2_Premium', parent=styles['Heading2'], textColor=colors.HexColor('#0B2D5C'), spaceBefore=20, spaceAfter=8, fontSize=13)
    style_h3 = ParagraphStyle('Heading3_Sub', parent=styles['Heading3'], textColor=colors.HexColor('#1F618D'), spaceBefore=15, spaceAfter=6, fontSize=11, fontName='Helvetica-Bold')
    style_flowchart = ParagraphStyle('Flowchart', parent=styles['Normal'], textColor=colors.HexColor('#117A65'), alignment=TA_CENTER, spaceBefore=8, spaceAfter=8, fontSize=10, fontName='Helvetica-Bold')
    
    # ESTILO FORÇADO PARA CABEÇALHO BRANCO NA TABELA
    style_table_header = ParagraphStyle('TableHeader', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold', fontSize=10, alignment=TA_CENTER)
    
    story = []
    texto_formatado = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    for emoji in ['💊', '🩺', '⚠️', '📈', '📚', '🌍', '⚖️', '📌', '📊', '📖', '🔀']: texto_formatado = texto_formatado.replace(emoji, '')
        
    linhas = texto_formatado.split('\n')
    table_data = []
    in_table = False
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            if in_table and table_data:
                t = Table(table_data, hAlign='LEFT', colWidths=[120, 180, 220])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2D5C')),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FDFEFE')),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D5D8DC')),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(t)
                story.append(Spacer(1, 15)) # Espaço maior após a tabela
                table_data = []
                in_table = False
            continue
            
        if '|' in linha:
            if '---' in linha: continue
            # Se for a primeira linha (cabeçalho), aplica a fonte branca forçada
            if not table_data:
                row = [Paragraph(cell.strip(), style_table_header) for cell in linha.split('|') if cell.strip()]
            else:
                row = [Paragraph(cell.strip(), style_normal) for cell in linha.split('|') if cell.strip()]
            if row: table_data.append(row)
            in_table = True
        else:
            if in_table and table_data:
                t = Table(table_data, hAlign='LEFT', colWidths=[120, 180, 220])
                t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2D5C')), ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FDFEFE')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D5D8DC'))]))
                story.append(t)
                story.append(Spacer(1, 15))
                table_data = []
                in_table = False
                
            if '➔' in linha or '->' in linha: story.append(Paragraph(linha, style_flowchart))
            elif linha.startswith('### '): story.append(Paragraph(linha.replace('### ', '').strip(), style_h3))
            elif linha.startswith('## ') or linha.startswith('1. ') or linha.startswith('2. ') or linha.startswith('3. '): 
                story.append(Spacer(1, 10)) # Espaço extra antes de cada novo bloco
                story.append(Paragraph(linha.replace('## ', '').strip(), style_h2))
            elif linha.startswith('- ') or linha.startswith('* '): story.append(Paragraph(f"• {linha[2:]}", style_normal))
            else: story.append(Paragraph(linha, style_normal))
            
    doc.build(story, onFirstPage=lambda c, d: add_premium_header_footer(c, d, email), onLaterPages=lambda c, d: add_premium_header_footer(c, d, email))
    buffer.seek(0)
    return buffer
