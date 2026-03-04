import streamlit as st
import google.generativeai as genai
import json
import re
import base64
from io import BytesIO
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
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
    Aja como um Professor Titular de Harvard Medical School.
    REGRA DE OURO: PROIBIDO TEXTOS LONGOS. Use esquemas, tabelas (Markdown), bullet points e frases curtas de alto impacto.
    Se o tema tiver subdivisões (Ex: IC Direita vs Esquerda), crie tópicos separados comparando etiologia, clínica e tratamento.
    
    Estrutura VISUAL e OBRIGATÓRIA:
    1. 📌 VISÃO GRANULAR: O que é e seus Subtipos (Fisiopatologia direta ao ponto).
    2. 📊 FLUXOGRAMA DE DECISÃO (Passo a Passo):
       - Passo 1: Avaliação Inicial...
       - Passo 2: Conduta X se Y...
    3. ⚖️ TABELA DE DIAGNÓSTICO DIFERENCIAL: Compare a doença alvo com suas principais confundidoras (Sinais clássicos vs Ignorados).
    4. 🌍 DIRETRIZES COMPARADAS: Diferenças-chave entre Brasil (SBC/AMB), EUA (AHA/ACC) e Europa (ESC).
    5. ⚠️ RED FLAGS & ARMADILHAS (Pitfalls).
    6. 📚 REFERÊNCIAS (Vancouver Estrito): Máx 8 anos. Inclua DOI.
    
    Adicione OBRIGATORIAMENTE no final esta exata linha:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    """
    try:
        from groq import Groq
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt}],
            temperature=0.2 # Mais frio = Mais objetivo e esquemático
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
    """Cabeçalho e Rodapé de Alto Padrão (Enterprise)"""
    canvas.saveState()
    # Cabeçalho Fixo
    canvas.setFillColor(colors.HexColor('#0B2D5C'))
    canvas.rect(0, 740, 612, 52, fill=1, stroke=0) # Barra Azul Topo
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 18)
    canvas.drawString(40, 760, "CORE NEXUS")
    canvas.setFont('Helvetica', 10)
    canvas.drawString(40, 748, "Clinical Guidelines & Advanced Pathways")
    
    # Rodapé Invisível/Discreto (Rastreio)
    codigo_rastreio = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    canvas.setFont('Helvetica', 6)
    canvas.setFillGray(0.7)
    canvas.drawString(40, 20, f"ID: CNX-{codigo_rastreio[:15]} | Validated Document | {datetime.datetime.now().strftime('%Y-%m-%d')}")
    canvas.restoreState()

def gerar_pdf_resposta(texto, email):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=70, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Normal_Bullet', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=8, fontSize=10, leading=14)
    style_h2 = ParagraphStyle('Heading2_Premium', parent=styles['Heading2'], textColor=colors.HexColor('#0B2D5C'), spaceBefore=15, spaceAfter=8, fontSize=14, borderPadding=4)
    style_h3 = ParagraphStyle('Heading3_Sub', parent=styles['Heading3'], textColor=colors.HexColor('#2E86C1'), spaceBefore=10, spaceAfter=5, fontSize=12)
    
    story = []
    
    # Tratamento Avançado de Markdown para o PDF
    linhas = texto.split('\n')
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        # Tratamento de Negritos
        linha = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', linha)
        linha = linha.replace('💊', '').replace('🩺', '').replace('⚠️', '').replace('📈', '').replace('📚', '').replace('🌍', '').replace('⚖️', '').replace('📌', '').replace('📊', '')
        
        # Parse de Cabeçalhos (H2 e H3)
        if linha.startswith('### '):
            story.append(Paragraph(linha.replace('### ', '').strip(), style_h3))
        elif linha.startswith('## ') or linha.startswith('1. ') or linha.startswith('2. ') or linha.startswith('3. '):
            story.append(Paragraph(linha.replace('## ', '').strip(), style_h2))
        elif linha.startswith('- ') or linha.startswith('* '):
            # Bullet points simulados
            story.append(Paragraph(f"• {linha[2:]}", style_normal))
        elif "|" in linha and "---" not in linha:
            # Captura grosseira de linhas de tabela para não quebrar o design
            story.append(Paragraph(f"<i>{linha}</i>", style_normal))
        elif "---" in linha:
            pass # Ignora divisores de markdown puro
        else:
            story.append(Paragraph(linha, style_normal))
            
    doc.build(story, onFirstPage=lambda c, d: add_premium_header_footer(c, d, email), onLaterPages=lambda c, d: add_premium_header_footer(c, d, email))
    
    buffer.seek(0)
    return buffer
