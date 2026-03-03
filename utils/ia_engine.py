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
    instrucao = """
    Aja como Preceptor Sênior. Estrutura:
    1. 💊 Conduta Imediata
    2. 📈 Escores e Critérios
    3. 🩺 Caso Clínico Simulado
    4. ⚠️ Red Flags
    5. 📚 Referências REAIS (VANCOUVER).
    
    Adicione OBRIGATORIAMENTE no final esta exata linha:
    TAGS_GERADAS: [Grande Área] | [Subtema]
    """
    
    # 1. TENTATIVA GROQ (Motor Principal - Ideal para Casos Clínicos sem censura)
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
        
        # Extração Perfeita de Tags
        if "TAGS_GERADAS:" in res:
            partes = res.split("TAGS_GERADAS:")
            texto_principal = partes[0].strip()
            tags = partes[1].split("|")
            area = tags[0].strip() if len(tags) > 0 else "Geral"
            subtema = tags[1].strip() if len(tags) > 1 else "Geral"
        else:
            texto_principal, area, subtema = res, "Clínica Médica", "Geral"
            
        return texto_principal, area, subtema
        
    except Exception as e_groq:
        # 2. TENTATIVA GEMINI (Fallback)
        try:
            model = configurar_gemini()
            if model:
                res = model.generate_content(f"{instrucao}\n\nPergunta: {prompt}").text
                if "TAGS_GERADAS:" in res:
                    partes = res.split("TAGS_GERADAS:")
                    texto_principal = partes[0].strip()
                    tags = partes[1].split("|")
                    area = tags[0].strip() if len(tags) > 0 else "Geral"
                    subtema = tags[1].strip() if len(tags) > 1 else "Geral"
                else:
                    texto_principal, area, subtema = res, "Clínica Médica", "Geral"
                return texto_principal, area, subtema
        except Exception as e_gemini:
            return f"Erro nos motores de IA. \nGroq: {e_groq}\nGemini: {e_gemini}", "Erro", "Erro"

def gerar_apenas_flashcards(texto, area, subtema, email):
    model = configurar_gemini()
    prompt = f"Gere 3 flashcards baseados no texto. Retorne apenas JSON: [{{\"p\": \"pergunta\", \"r\": \"resposta\"}}]. Texto: {texto}"
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
    prompt = f"Gere 2 questões ABCD. JSON: [{{\"pergunta\": \"\", \"a\": \"\", \"b\": \"\", \"c\": \"\", \"d\": \"\", \"gabarito\": \"A\", \"justificativa\": \"\"}}]. Texto: {texto}"
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
    p.drawString(50, 750, "CORE NEXUS - Relatório de Conduta Clínica")
    p.setFont("Helvetica", 10)
    
    textobject = p.beginText(50, 730)
    # Limpeza básica do texto para não quebrar o PDF
    texto_limpo = texto.replace('**', '').replace('💊', '').replace('🩺', '').replace('⚠️', '').replace('📈', '').replace('📚', '')
    for line in texto_limpo.split('\n'):
        # Quebra de linha simples para caber na página
        while len(line) > 100:
            textobject.textLine(line[:100])
            line = line[100:]
        textobject.textLine(line)
        
    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
