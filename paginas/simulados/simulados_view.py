import streamlit as st
from utils.ia_engine import processar_arquivo_para_estudo
from database import salvar_questao_banco

def show():
    st.markdown("### 📄 Dissecador de Arquivos | Provas de Elite")
    
    uploaded_file = st.file_uploader("Suba uma Diretriz, Artigo ou Resumo (PDF/TXT):", type=['pdf', 'txt'])
    
    if uploaded_file:
        if st.button("Gerar Banco de Questões Dissecado ⚡"):
            with st.status("IA lendo arquivo e mapeando distratores...", expanded=True):
                # Aqui simplificamos a leitura (em prod usaríamos PyPDF2)
                conteudo = uploaded_file.read().decode("utf-8", errors="ignore")
                questoes = processar_arquivo_para_estudo(conteudo, st.session_state.user_email)
                
                if questoes:
                    st.session_state.questoes_dissecadas = questoes
                    st.success(f"{len(questoes)} Questões de alto nível geradas!")

    if 'questoes_dissecadas' in st.session_state:
        for idx, q in enumerate(st.session_state.questoes_dissecadas):
            with st.container(border=True):
                st.markdown(f"**Q{idx+1}: {q['pergunta']}**")
                resp = st.radio(f"Escolha sua resposta (Q{idx+1}):", ["A", "B", "C", "D"], key=f"file_q_{idx}")
                
                if st.button(f"Validar Q{idx+1}", key=f"val_btn_{idx}"):
                    if resp == q['gabarito']:
                        st.success(f"✅ CORRETO! {q['justificativa_correta']}")
                    else:
                        st.error(f"❌ INCORRETO. O gabarito é {q['gabarito']}.")
                        st.markdown(f"**Por que você errou:** {q['comentario_distratores'][resp]}")
                        st.warning(f"📚 **Onde focar:** {q['area_reforco']}")
                    
                    with st.expander("Ver análise completa de todas as alternativas"):
                        for alt, coment in q['comentario_distratores'].items():
                            st.write(f"**{alt}:** {coment}")
