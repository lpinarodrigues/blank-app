import streamlit as st
import pandas as pd
from shared_logic import recuperar_logs, tem_permissao

def show():
    if not tem_permissao("Admin"):
        st.error("Acesso restrito à Diretoria.")
        return

    st.title("🛡️ Painel de Governança")
    
    st.markdown("### 🔍 Trilha de Auditoria (Blockchain-like)")
    logs = recuperar_logs()
    
    if logs:
        df = pd.DataFrame(logs, columns=["Data/Hora", "Usuário", "Atividade", "Hash de Segurança"])
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exportar Relatório de Auditoria", csv, "nexus_audit.csv", "text/csv")
    else:
        st.info("Nenhum log registrado no banco de dados ainda.")

    st.markdown("---")
    st.markdown("#### 👥 Gestão de Whitelist")
    st.write("Em breve: Interface para autorizar novos e-mails da UNIFESP.")
