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

def consultar_core_ia_perfeicao(prompt):
    instrucao = """
    Aja como um Preceptor Titular de Harvard (Attending Physician).
    
    DIRETRIZES DE TRIANGULAÇÃO E QUALIDADE (MANDATÓRIO):
    1. ZERO ERROS DE ESCRITA: Revise mentalmente a ortografia (PT-BR) e a gramática antes de gerar a saída.
    2. ZERO GENERALIZAÇÃO: Se a doença possui lados, subtipos ou perfis (ex: IC Direita vs Esquerda; Perfil Quente/Úmido), EXPLIQUE CADA UM SEPARADAMENTE. Detalhe os sinais exatos de cada subtipo.
    
    ESTRUTURA VISUAL E TÉCNICA OBRIGATÓRIA:
    1. 📌 FISIOPATOLOGIA E SUBTIPOS: Quebre a doença. (Ex: O que causa a falha direita? Turgência jugular, hepatomegalia. O que causa a esquerda? Estertores, ortopneia).
    2. 🔀 FLUXOGRAMA DE DECISÃO VISUAL: Crie um algoritmo passo-a-passo usando setas.
       Exemplo: [Sintoma] ➔ [Sinal de Alerta] ➔ [Exame] ➔ [Conduta Específica].
    3. ⚖️ DIAGNÓSTICO DIFERENCIAL (TABELA): 
       Crie uma tabela Markdown estrita com 3 colunas:
       | Doença Confundidora | Sintomas Semelhantes (O que confunde) | Sinal Diferenciador / Patognomônico (Como excluir) |
    4. 📈 ESCORES E CRITÉRIOS: Destrinche os parâmetros (O que pontua e qual a conduta por faixa).
    5. ⚠️ RED FLAGS & PITFALLS: Erros comuns do plantonista.
    6. 📖 GLOSSÁRIO RÁPIDO: Defina 3 termos ultra-técnicos usados.
    7. 📚 REFERÊNCIAS: Padrão Vancouver (máx 8 anos, inclua DOI).
    
    Adicione OBRIGATORIAMENTE no final esta exata linha:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    """
    try:
        from groq import Groq
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt}],
            temperature=0.15 # Reduzido para focar na precisão extrema e evitar alucinações gramaticais
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
    prompt = f"Gere 5 flashcards avançados. JSON: [{{\"p\": \"pergunta\", \"r\": \"resposta\"}}]. Texto: {texto}"
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
    prompt = f"Gere 3 questões de residência ABCD. JSON: [{{\"pergunta\": \"\", \"a\": \"\", \"b\": \"\", \"c\": \"\", \"d\": \"\", \"gabarito\": \"A\", \"justificativa\": \"\"}}]. Texto: {texto}"
    try:
        res = model.generate_content(prompt).text
        dados = extrair_json_seguro(res)
        from database import salvar_questao
        count = 0
        for q in dados:
            if salvar_questao({"pergunta": q['pergunta'], "opcao_a": q['a'], "opcao_b": q['b'], "opcao_c": q['c'], "opcao_d": q['d'], "gabarito": q['gabarito'], "explica_correta": q['justificativa'], "grande_area": area, "subtema": subtema, "is_global": True}): count+=1
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
    # NOVA ESTÉTICA: Cinza Chumbo (#2C3E50) em vez de Preto, tamanho ideal para leitura.
    style_normal = ParagraphStyle('Normal_Bullet', parent=styles['Normal'], textColor=colors.HexColor('#2C3E50'), alignment=TA_JUSTIFY, spaceAfter=8, fontSize=10, leading=15)
    style_h2 = ParagraphStyle('Heading2_Premium', parent=styles['Heading2'], textColor=colors.HexColor('#0B2D5C'), spaceBefore=12, spaceAfter=6, fontSize=13)
    style_h3 = ParagraphStyle('Heading3_Sub', parent=styles['Heading3'], textColor=colors.HexColor('#1F618D'), spaceBefore=8, spaceAfter=4, fontSize=11, fontName='Helvetica-Bold')
    # ESTILO DO FLUXOGRAMA
    style_flowchart = ParagraphStyle('Flowchart', parent=styles['Normal'], textColor=colors.HexColor('#117A65'), alignment=TA_CENTER, spaceBefore=4, spaceAfter=4, fontSize=10, fontName='Helvetica-Bold', borderPadding=5)
    
    story = []
    texto_formatado = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    for emoji in ['💊', '🩺', '⚠️', '📈', '📚', '🌍', '⚖️', '📌', '📊', '📖', '🔀']:
        texto_formatado = texto_formatado.replace(emoji, '')
        
    linhas = texto_formatado.split('\n')
    table_data = []
    in_table = False
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            if in_table and table_data:
                t = Table(table_data, hAlign='LEFT', colWidths=[120, 180, 220]) # Ajuste dinâmico das colunas da Tabela de DDx
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2D5C')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 9),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FDFEFE')), # Fundo da tabela super claro
                    ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2C3E50')),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D5D8DC')), # Linhas de grade suaves
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(t)
                story.append(Spacer(1, 10))
                table_data = []
                in_table = False
            continue
            
        if '|' in linha:
            if '---' in linha: continue
            row = [Paragraph(cell.strip(), style_normal) for cell in linha.split('|') if cell.strip()]
            if row: table_data.append(row)
            in_table = True
        else:
            if in_table and table_data:
                # Renderizar tabela residual
                t = Table(table_data, hAlign='LEFT', colWidths=[120, 180, 220])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2D5C')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 9),
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FDFEFE')),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D5D8DC')),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ]))
                story.append(t)
                story.append(Spacer(1, 10))
                table_data = []
                in_table = False
                
            # Identificador de Fluxograma (Se tiver setas)
            if '➔' in linha or '->' in linha:
                story.append(Paragraph(linha, style_flowchart))
            elif linha.startswith('### '): story.append(Paragraph(linha.replace('### ', '').strip(), style_h3))
            elif linha.startswith('## ') or linha.startswith('1. ') or linha.startswith('2. '): story.append(Paragraph(linha.replace('## ', '').strip(), style_h2))
            elif linha.startswith('- ') or linha.startswith('* '): story.append(Paragraph(f"• {linha[2:]}", style_normal))
            else: story.append(Paragraph(linha, style_normal))
            
    if in_table and table_data:
        t = Table(table_data, hAlign='LEFT', colWidths=[120, 180, 220])
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B2D5C')), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D5D8DC'))]))
        story.append(t)
        
    doc.build(story, onFirstPage=lambda c, d: add_premium_header_footer(c, d, email), onLaterPages=lambda c, d: add_premium_header_footer(c, d, email))
    buffer.seek(0)
    return buffer
