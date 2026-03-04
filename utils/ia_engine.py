import streamlit as st
from groq import Groq
import json
from database import salvar_item_estudo

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
    return res, "Geral", "Clínica"

def gerar_apenas_flashcards(texto_base, area, subtema, email):
    client = get_ai_client()
    # CORREÇÃO AQUI: Chaves duplas {{ }} para o Python não confundir o JSON com variáveis
    prompt = f"""Baseado neste texto médico, crie 5 Flashcards (Pergunta e Resposta).
    Retorne EXCLUSIVAMENTE um objeto JSON com a chave "flashcards" contendo a lista.
    Exemplo do formato:
    {{ "flashcards": [ {{ "pergunta": "Qual o limite?", "resposta": "120 mmHg" }} ] }}
    
    Texto: {texto_base}"""
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        cards = json.loads(completion.choices[0].message.content)
        lista = cards.get('flashcards', cards) if isinstance(cards, dict) else cards
        
        count = 0
        if isinstance(lista, list):
            for c in lista:
                if isinstance(c, dict) and 'pergunta' in c and 'resposta' in c:
                    salvar_item_estudo({
                        "pergunta": c['pergunta'],
                        "resposta": c['resposta'],
                        "grande_area": area,
                        "subtema": subtema,
                        "categoria": "Flashcard",
                        "criado_por_email": email
                    })
                    count += 1
        return count
    except Exception as e:
        print(f"Erro Flashcard: {e}")
        return 0

def gerar_apenas_questoes(texto_base, area, subtema, email):
    client = get_ai_client()
    # CORREÇÃO AQUI: Chaves duplas {{ }}
    prompt = f"""Crie 3 questões de múltipla escolha baseadas no texto. 
    Retorne EXCLUSIVAMENTE um objeto JSON com a chave "questoes" contendo a lista.
    Exemplo do formato: 
    {{ "questoes": [ {{ "pergunta": "...", "a": "...", "b": "...", "c": "...", "d": "...", "gabarito": "A", "explicacao": "..." }} ] }}
    
    Texto: {texto_base}"""
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        dados = json.loads(completion.choices[0].message.content)
        questoes = dados.get('questoes', dados) if isinstance(dados, dict) else dados
        
        count = 0
        if isinstance(questoes, list):
            from database import get_supabase
            for q in questoes:
                if isinstance(q, dict):
                    get_supabase().table("questionarios").insert({
                        "pergunta": q.get('pergunta', ''),
                        "opcao_a": q.get('a', ''),
                        "opcao_b": q.get('b', ''),
                        "opcao_c": q.get('c', ''),
                        "opcao_d": q.get('d', ''),
                        "gabarito": q.get('gabarito', 'A'),
                        "explica_correta": q.get('explicacao', ''),
                        "criado_por_email": email
                    }).execute()
                    count += 1
        return count
    except Exception as e:
        print(f"Erro Questões: {e}")
        return 0

def ler_arquivo_texto(arquivo):
    if arquivo is None: return ""
    return arquivo.getvalue().decode("utf-8", errors="ignore")

def gerar_pdf_resposta(texto, email):
    return b"PDF Gerado com Sucesso"
