import streamlit as st
from groq import Groq
import json
import io
import PyPDF2
import docx
import pptx
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database import salvar_item_estudo

def get_ai_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def consultar_core_ia_perfeicao(prompt, contexto="", img_b64=None):
    client = get_ai_client()
    sys_msg = "Você é o CORE NEXUS. Responda de forma clínica, objetiva e baseada em evidências."
    full_prompt = f"Contexto do Arquivo: {contexto}\n\nPergunta/Comando: {prompt}"
    
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
    
    if texto.startswith(marca_json):
        texto = texto[7:]
    elif texto.startswith(marca_simples):
        texto = texto[3:]
        
    if texto.endswith(marca_simples):
        texto = texto[:-3]
        
    return texto.strip()

def gerar_apenas_flashcards(texto_base, area, subtema, email, qtd=5):
    client = get_ai_client()
    prompt = (
        f"Baseado no texto, crie {qtd} Flashcards.\n"
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
                    salvar_item_estudo({
                        "pergunta": c["pergunta"],
                        "resposta": c["resposta"],
                        "grande_area": area,
                        "subtema": subtema,
                        "categoria": "Flashcard",
                        "criado_por_email": email
                    })
                    count += 1
        return count
    except Exception as e:
        print(f"Erro FC: {e}")
        return 0

def gerar_apenas_questoes(texto_base, area, subtema, email, qtd=3):
    client = get_ai_client()
    prompt = (
        f"Crie {qtd} questoes de multipla escolha.\n"
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
                    get_supabase().table("questionarios").insert({
                        "pergunta": q.get("pergunta", ""),
                        "opcao_a": q.get("a", ""),
                        "opcao_b": q.get("b", ""),
                        "opcao_c": q.get("c", ""),
                        "opcao_d": q.get("d", ""),
                        "gabarito": q.get("gabarito", "A"),
                        "explica_correta": q.get("explicacao", ""),
                        "criado_por_email": email
                    }).execute()
                    count += 1
        return count
    except Exception as e:
        print(f"Erro QS: {e}")
        return 0

def ler_documento_universal(arquivo):
    if arquivo is None: return ""
    nome = arquivo.name.lower()
    try:
        if nome.endswith(".txt"): return arquivo.getvalue().decode("utf-8", errors="ignore")
        elif nome.endswith(".pdf"):
            pdf = PyPDF2.PdfReader(arquivo)
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif nome.endswith(".docx"):
            doc = docx.Document(arquivo)
            return " ".join([p.text for p in doc.paragraphs])
        elif nome.endswith(".pptx"):
            ppt = pptx.Presentation(arquivo)
            texto = []
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"): texto.append(shape.text)
            return " ".join(texto)
    except Exception as e: return f"Erro ao ler arquivo: {e}"
    return ""

def gerar_pdf_premium(texto, titulo="Protocolo Nexus"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "CORE NEXUS | Inteligência Médica")
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, titulo)
    c.line(50, 710, 550, 710)
    
    y = 680
    c.setFont("Helvetica", 10)
    for linha in texto.split("\n"):
        if len(linha) > 90:
            c.drawString(50, y, linha[:90] + "...")
        else:
            c.drawString(50, y, linha)
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
            c.setFont("Helvetica", 10)
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()