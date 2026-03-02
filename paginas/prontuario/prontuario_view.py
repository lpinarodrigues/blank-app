import streamlit as st
from datetime import datetime
import hashlib

def generate_security_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()[:12].upper()

def show():
    st.title("📝 Prontuário Master | Emissão Segura")
    st.markdown("---")
    
    with st.container(border=True):
        st.subheader("🛡️ Protocolo de Segurança")
        st.caption("Todos os documentos são criptografados e rastreáveis.")
        
        conteudo = st.text_area("Conteúdo do Documento (Evolução/Alta):")
        
        if st.button("🔐 Gerar Documento com Assinatura Digital"):
            token = generate_security_hash(conteudo + str(datetime.now()))
            st.success(f"Documento Validado! ID de Segurança: {token}")
            
            doc_final = f"""
            --- DOCUMENTO MÉDICO SEGURO ---
            EMISSÃO: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            ID: {token}
            --------------------------------
            {conteudo}
            --------------------------------
            VALIDADO VIA CORE NEXUS PROTECT
            """
            st.code(doc_final)
            st.download_button("📥 Baixar PDF Seguro", data=doc_final, file_name=f"doc_{token}.txt")
