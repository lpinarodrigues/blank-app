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
    instrucao = """
    Aja como um Preceptor Médico de Excelência. 
    Estrutura da Resposta:
    1. 💊 Conduta Imediata (Linha a linha).
    2. 📈 Escores e Critérios (Ex: CHA2DS2-VASc, CURB-65).
    3. 🩺 Caso Clínico Simulado (Breve).
    4. ⚠️ Red Flags.
    5. 📚 Referências REAIS em formato VANCOUVER.
    
    Proibido citar nomes de instituições ou empresas.
    """
    if model:
        try:
            res = model.generate_content(f"{instrucao}\n\nPergunta: {prompt}").text
            return res, "💎 Resposta Estruturada"
        except: return "Erro no processamento da IA.", "❌ Erro"
    return "Erro de configuração de chaves.", "❌ Erro"

def gerar_batch_flashcards(texto, tema, email):
    """Gera 10 flashcards e 5 questões baseados no conteúdo"""
    model = configurar_gemini()
    prompt = f"""
    Baseado no texto médico abaixo, gere:
    - 10 Flashcards (p: pergunta, r: resposta)
    - 5 Questões (pergunta, a, b, c, d, gabarito, justificativa)
    Retorne APENAS um JSON com as chaves 'flashcards' e 'questoes'.
    Texto: {texto}
    """
    try:
        res = model.generate_content(prompt).text
        dados = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_item_estudo
        
        count = 0
        for f in dados.get('flashcards', []):
            salvar_item_estudo({
                "pergunta": f['p'], "resposta": f['r'], "grande_area": "Geral",
                "subtema": tema, "is_global": True, "criado_por_email": email
            })
            count += 1
        return count
    except:
        return 0

def gerar_pdf_resposta(texto):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 750, "CORE NEXUS - Relatório de Conduta Clínica")
    p.setFont("Helvetica", 10)
    
    textobject = p.beginText(100, 730)
    for line in texto.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
