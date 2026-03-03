import streamlit as st
import google.generativeai as genai
from groq import Groq
import random

def consultar_core_ia_perfeicao(prompt, modo="Beira de Leito"):
    # Configuração do Prompt Sistêmico (DNA Dante Pazzanese/UpToDate)
    instrucao = f"""
    Aja como um Preceptor Sênior de Cardiologia. 
    Sua resposta deve seguir o padrão de medicina baseada em evidências.
    MODO: {modo}
    
    REGRAS OBRIGATÓRIAS:
    1. Sempre cite a Classe de Recomendação (Ex: Classe I) e Nível de Evidência (Ex: Nível A).
    2. Identifique contraindicações críticas.
    3. Cite a fonte (Ex: Diretriz SBC 2024, ESC 2023).
    4. No modo 'Beira de Leito', use listas curtas. No modo 'Acadêmico', seja exaustivo.
    """
    
    try:
        # Uso do Groq para velocidade de raciocínio lógico
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res_groq = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": instrucao},
                {"role": "user", "content": prompt}
            ],
        ).choices[0].message.content

        return res_groq, "✅ Fontes: SBC/ESC/AHA Processadas."
    except Exception as e:
        return f"Erro na análise: {e}", "⚠️ Falha de conexão."
