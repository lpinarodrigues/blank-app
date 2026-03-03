import streamlit as st
import google.generativeai as genai
import json
import re
from io import BytesIO
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
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
    1. 💊 Conduta Imediata e Fisiopatologia (Detalhe doses, vias e mecanismos).
    2. 📈 Escores e Critérios Diagnósticos (Explique a pontuação e conduta para cada estrato).
    3. 🩺 Caso Clínico Simulado (Completo: anamnese, exame físico, laboratório e desfecho).
    4. ⚠️ Red Flags e Complicações Potenciais.
    5. 📚 Referências REAIS (ESTRITAMENTE PADRÃO VANCOUVER). 
       - Exemplo Artigo: Autores. Título do Artigo. Título da Revista. Ano;Volume(Número):Páginas iniciais-finais. DOI: 10...
       - Exemplo Livro: Autores do Capítulo. Título do Capítulo. In: Autores do Livro. Título do Livro. Edição. Cidade: Editora; Ano. p. Página inicial-final.
    
    Adicione OBRIGATORIAMENTE no final esta exata linha:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    """
    
    try:
        from groq import Groq
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": instrucao},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        ).choices[0].message.content
        
        if "TAGS_GERADAS:" in res:
            partes = res.split("TAGS_GERADAS:")
            texto_principal = partes[0].strip()
            tags = partes[1].split("|")
            area = tags[0].strip() if len(tags) > 0 else "Geral"
            subtema = tags[1].strip() if len(tags) > 1 else "Geral"
        else:
            texto_principal, area, subtema = res, "Clínica Médica", "Geral"
            
        return texto_principal, area, subtema
    except Exception as e:
        return f"Erro no processamento: {e}", "Erro", "Erro"

def extrair_json_seguro(texto):
    """Garante a extração do JSON mesmo que a IA coloque texto antes ou depois"""
    try:
        match = re.search(r'\[\s*\{.*?\}\s*\]', texto, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(texto)
    except:
        return []

def gerar_apenas_flashcards(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 5 flashcards avançados sobre o texto. Retorne APENAS o JSON no formato exato: [{{\"p\": \"pergunta\", \"r\": \"resposta\"}}]. Sem texto adicional. Texto: {texto}"
    try:
        res = model.generate_content(prompt).text
        dados = extrair_json_seguro(res)
        from database import salvar_item_estudo
        count = 0
        for f in dados:
            if salvar_item_estudo({"pergunta": f['p'], "resposta": f['r'], "grande_area": area, "subtema": subtema, "categoria": "Flashcard", "is_global": True, "criado_por_email": email}):
                count += 1
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
            if salvar_questao({"pergunta": q['pergunta'], "opcao_a": q['a'], "opcao_b": q['b'], "opcao_c": q['c'], "opcao_d": q['d'], "gabarito": q['gabarito'], "explica_correta": q['justificativa'], "grande_area": area, "subtema": subtema, "is_global": True}):
                count += 1
        return count
    except: return 0

def add_watermark(canvas, doc, email):
    """Adiciona código de rastreabilidade (Watermark) em todas as páginas"""
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 14)
    canvas.setFillGray(0.5, 0.3) # Transparência para não atrapalhar a leitura
    canvas.translate(300, 400)
    canvas.rotate(45)
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    canvas.drawCentredString(0, 0, f"DOCUMENTO RASTREADO: {email.upper()} - {data_hora}")
    canvas.restoreState()

def gerar_pdf_resposta(texto, email):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('Normal_Justify', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=10, fontSize=11, leading=14)
    style_title = ParagraphStyle('Title_Center', parent=styles['Heading1'], alignment=1, spaceAfter=20)
    
    story = []
    story.append(Paragraph("CORE NEXUS - Protocolo Clínico", style_title))
    
    # Tratamento simples do Markdown para o PDF
    texto_limpo = texto.replace('**', '').replace('💊', '').replace('🩺', '').replace('⚠️', '').replace('📈', '').replace('📚', '')
    
    for paragrafo in texto_limpo.split('\n\n'):
        if paragrafo.strip():
            story.append(Paragraph(paragrafo.replace('\n', '<br/>'), style_normal))
            story.append(Spacer(1, 10))
            
    # Gera o PDF passando a função de Watermark
    doc.build(story, onFirstPage=lambda canvas, doc: add_watermark(canvas, doc, email), onLaterPages=lambda canvas, doc: add_watermark(canvas, doc, email))
    
    buffer.seek(0)
    return buffer
