import streamlit as st
from groq import Groq
import google.generativeai as genai
import json
import re
from database import salvar_item_estudo, salvar_questao

# Configuração das chaves
def get_ai_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def consultar_core_ia_perfeicao(prompt, contexto="", img_b64=None):
    client = get_ai_client()
    sys_msg = "Você é o CORE NEXUS. Responda de forma clínica, objetiva e baseada em evidências."
    full_prompt = f"Contexto: {contexto}\n\nPergunta: {prompt}"
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": full_prompt}],
        temperature=0.3
    )
    res = completion.choices[0].message.content
    # Lógica simplificada para extrair área e subtema
    return res, "Geral", "Clínica"

def gerar_apenas_flashcards(texto_base, area, subtema, email):
    client = get_ai_client()
    prompt = f"""Baseado neste texto médico, crie 5 Flashcards (Pergunta e Resposta).
    Formato OBRIGATÓRIO (JSON):
    [{"pergunta": "...", "resposta": "..."}]
    Texto: {texto_base}"""
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        cards = json.loads(completion.choices[0].message.content)
        # Se a IA retornar um dicionário com uma chave 'flashcards'
        lista = cards.get('flashcards', cards) if isinstance(cards, dict) else cards
        
        for c in lista:
            salvar_item_estudo({
                "pergunta": c['pergunta'],
                "resposta": c['resposta'],
                "grande_area": area,
                "subtema": subtema,
                "categoria": "Flashcard",
                "criado_por_email": email
            })
        return len(lista)
    except:
        return 0

def gerar_apenas_questoes(texto_base, area, subtema, email):
    client = get_ai_client()
    prompt = f"""Crie 3 questões de múltipla escolha baseadas no texto. 
    Formato JSON: 
    [{"pergunta": "...", "a": "...", "b": "...", "c": "...", "d": "...", "gabarito": "A/B/C/D", "explicacao": "..."}]
    Texto: {texto_base}"""
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        dados = json.loads(completion.choices[0].message.content)
        questoes = dados.get('questoes', dados) if isinstance(dados, dict) else dados
        
        for q in questoes:
            # Função para salvar na tabela específica de questões
            from database import get_supabase
            get_supabase().table("questionarios").insert({
                "pergunta": q['pergunta'],
                "opcao_a": q['a'],
                "opcao_b": q['b'],
                "opcao_c": q['c'],
                "opcao_d": q['d'],
                "gabarito": q['gabarito'],
                "explica_correta": q['explicacao'],
                "criado_por_email": email,
                "categoria": "Questão"
            }).execute()
        return len(questoes)
    except:
        return 0

def ler_arquivo_texto(arquivo):
    if arquivo is None: return ""
    return arquivo.getvalue().decode("utf-8", errors="ignore")

def gerar_pdf_resposta(texto, email):
    # Lógica simplificada de PDF para evitar erro de importação
    return b"PDF Content"
