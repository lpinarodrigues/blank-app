import streamlit as st
import base64
from utils.ia_engine import (
    consultar_core_ia_perfeicao, gerar_apenas_flashcards, 
    gerar_apenas_questoes, gerar_pdf_resposta, ler_arquivo_texto
)
from database import salvar_item_estudo, salvar_historico_chat
# Nota: Removido shared_logic se não existir no seu repositório para evitar erro de import

# Custom CSS para visual "Premium Terminal"
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; transition: 0.3s; height: 3em; }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; }
    .st-emotion-cache-12w0qpk { padding: 1.5rem; background: #1e293b; border-radius: 12px; border-left: 4px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

def show():
    email = st.session_state.get('user_email', 'admin@nexus.com')
    
    st.markdown("### 🧠 Terminal Clínico Avançado | Oráculo Multimodal")
    
    # Área de Contexto (Uploads)
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        with st.expander("📎 Documento Base (PDF/Texto)", expanded=False):
            doc_upload = st.file_uploader("Upload de diretriz ou prontuário", type=["pdf", "docx", "txt"], key="doc_up")
    with col_up2:
        with st.expander("🖼️ Análise de Imagem (ECG/Lab)", expanded=False):
            foto_exame = st.file_uploader("Upload de imagem de exame", type=["jpg", "png", "jpeg"], key="img_up")

    # Inicialização do Estado
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ultima_resposta" not in st.session_state:
        st.session_state.ultima_resposta = None

    # Exibição do Histórico
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input do Chat
    if prompt := st.chat_input("Descreva o caso, dúvida ou conduta desejada..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sincronizando evidências..."):
                try:
                    texto_contexto = ler_arquivo_texto(doc_upload) if doc_upload else ""
                    img_b64 = None
                    if foto_exame:
                        img_b64 = base64.b64encode(foto_exame.getvalue()).decode()
                    
                    sys_prompt = "Aja como NEXUS CORE AI. Diagnósticos (Top 3), Scores e Conduta (Classe I)."
                    
                    # Chamada com 3 parâmetros
                    res, area, sub = consultar_core_ia_perfeicao(f"{sys_prompt}\n\n{prompt}", texto_contexto, img_b64)
                    
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    st.session_state.ultima_resposta = {"q": prompt, "a": res, "area": area, "sub": sub}
                    salvar_historico_chat(email, prompt, res, area, sub)
                except Exception as e:
                    st.error(f"Erro na conexão: {e}")

    # Ações Rápidas (Sempre Visíveis após a primeira resposta)
    if st.session_state.ultima_resposta:
        st.divider()
        dados = st.session_state.ultima_resposta
        st.markdown("#### 🛠️ Ações de Estudo e Exportação")
        c1, c2, c3, c4 = st.columns(4)
        
        if c1.button("📥 Salvar Resumo", key="btn_save"):
            salvar_item_estudo({"pergunta": dados['q'], "resposta": dados['a'], "grande_area": dados['area'], "subtema": dados['sub'], "categoria": "Resumo", "criado_por_email": email})
            st.toast("✅ Salvo na Biblioteca!")
        
        if c2.button("🎴 Flashcards", key="btn_cards"):
            qtd = gerar_apenas_flashcards(dados['a'], dados['area'], dados['sub'], email)
            st.toast(f"✅ {qtd} Cards gerados!")
            
        if c3.button("📝 Questões", key="btn_quest"):
            qtd = gerar_apenas_questoes(dados['a'], dados['area'], dados['sub'], email)
            st.toast(f"✅ Simulado criado!")

        try:
            pdf = gerar_pdf_resposta(dados['a'], email)
            c4.download_button("📄 PDF Premium", data=pdf, file_name="nexus_protocolo.pdf", key="btn_pdf")
        except:
            c4.button("📄 Erro PDF", disabled=True)
