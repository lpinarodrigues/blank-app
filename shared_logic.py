import streamlit as st
import requests
import datetime
import sqlite3
import hashlib

# --- BANCO DE DADOS ---
def inicializar_db():
    conn = sqlite3.connect('nexus_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS auditoria 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, usuario TEXT, atividade TEXT, hash TEXT)''')
    conn.commit()
    conn.close()

def salvar_log_auditoria(usuario, atividade, hash_id):
    conn = sqlite3.connect('nexus_data.db')
    c = conn.cursor()
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO auditoria (data, usuario, atividade, hash) VALUES (?, ?, ?, ?)", (data_atual, usuario, atividade, hash_id))
    conn.commit()
    conn.close()

def recuperar_logs():
    try:
        conn = sqlite3.connect('nexus_data.db')
        c = conn.cursor()
        c.execute("SELECT data, usuario, atividade, hash FROM auditoria ORDER BY id DESC LIMIT 50")
        logs = c.fetchall()
        conn.close()
        return logs
    except:
        return []

# --- SEGURANÇA ---
def gerar_codificacao_seguranca(usuario, atividade):
    seed = f"{usuario}{atividade}{datetime.datetime.now()}"
    return hashlib.sha256(seed.encode()).hexdigest()[:12].upper()

def tem_permissao(nivel_requerido):
    if "user_email" not in st.session_state: return False
    admins = ["lpinarodrigues@gmail.com"]
    return st.session_state.user_email in admins if nivel_requerido == "Admin" else True

def verificar_consentimento_lgpd(email):
    return st.session_state.get("lgpd_consent", False)

def registrar_aceite_lgpd(email):
    st.session_state.lgpd_consent = True

def obter_saudacao():
    hora = datetime.datetime.now().hour
    return "Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"

# --- INTELIGÊNCIA (FORÇANDO PORTUGUÊS) ---
def chamar_oraculo(pergunta):
    # Instrução Mestra de Idioma
    instrucao_idioma = " IMPORTANTE: Responda SEMPRE em Português do Brasil, de forma técnica e profissional. "
    prompt_final = f"{instrucao_idioma}\n\n{pergunta}"

    # TENTATIVA 1: GROQ
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt_final}]}
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
    except:
        pass

    # TENTATIVA 2: GEMINI
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt_final}]}]}
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        pass
    
    return "Erro de conexão. Por favor, tente novamente."

def lembrete_etico():
    return "⚠️ Suporte à decisão clínica. A responsabilidade é do médico assistente."
