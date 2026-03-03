import streamlit as st
import google.generativeai as genai
import json
import random

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
    instrucao = f"""
    Aja como um Preceptor Médico de Excelência. Modo: {modo}.
    Sua resposta DEVE seguir esta estrutura rigorosa:
    1. 💊 **Conduta Imediata** (Linha a linha).
    2. 📈 **Escores e Critérios** (Ex: CHADS-VASC, CURB-65, etc., quando aplicável).
    3. 🩺 **Caso Clínico Simulado** (Breve, para fixação).
    4. ⚠️ **Red Flags** (O que não pode passar batido).
    
    Proibido citar nomes de empresas ou instituições externas.
    """
    if model:
        res = model.generate_content(f"{instrucao}\n\nPergunta: {prompt}").text
        return res, "💎 Resposta Estruturada por IA"
    return "Erro de configuração de chaves.", "❌ Erro"

def gerar_batch_flashcards(texto, tema, email):
    model = configurar_gemini()
    prompt = f"""
    Baseado no texto abaixo, gere 10 Flashcards (Pergunta e Resposta) 
    E 5 Questões de múltipla escolha (A, B, C, D) com gabarito e justificativa.
    Retorne estritamente um JSON com as chaves: 'flashcards' e 'questoes'.
    Texto: {texto}
    """
    try:
        res = model.generate_content(prompt).text
        dados = json.loads(res.replace('```json', '').replace('```', '').strip())
        from database import salvar_item_estudo
        
        # Salva Flashcards
        for f in dados['flashcards']:
            salvar_item_estudo({
                "pergunta": f['p'], "resposta": f['r'], "grande_area": "Geral",
                "subtema": tema, "is_global": True, "criado_por_email": email
            })
        
        # Salva Questões (Banco de Big Data)
        for q in dados['questoes']:
            # Aqui você pode adicionar lógica para salvar na tabela de questionários
            pass
            
        return len(dados['flashcards']) + len(dados['questoes'])
    except:
        return 0
