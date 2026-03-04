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
    if texto.startswith("