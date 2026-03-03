import streamlit as st
from utils.ia_engine import gerar_questao_medica_ia
from database import salvar_questao_banco, listar_questoes_simulado, registrar_performance

def show():
    st.markdown('<h3 style="color: #1E3A8A;">📝 Simulados | Padrão SBC/TEC</h3>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✍️ Praticar Simulado", "🤖 Gerar Questões"])
    
    with tab2:
        st.subheader("Gerador de Questões de Elite")
        tema = st.text_input("Tema do Simulado:", placeholder="Ex: Valvopatias, Insuficiência Coronariana...")
        dif = st.select_slider("Dificuldade:", options=["Fácil", "Média", "Difícil"])
        
        if st.button("Gerar e Adicionar ao Banco ⚡"):
            with st.status("IA redigindo questão técnica...", expanded=True):
                questao = gerar_questao_medica_ia(tema, dif)
                if questao:
                    salvar_questao_banco(questao)
                    st.success("Questão gerada e salva com sucesso!")
                    st.json(questao)
                else:
                    st.error("Erro ao processar JSON da IA. Tente novamente.")

    with tab1:
        categoria = st.selectbox("Filtrar por Tema:", ["Geral", "Cardiologia", "Valvopatias", "Emergência"])
        questoes = listar_questoes_simulado(categoria)
        
        if not questoes:
            st.info("Nenhuma questão disponível neste tema. Gere uma na aba ao lado!")
        else:
            if 'respostas' not in st.session_state: st.session_state.respostas = {}
            
            acertos = 0
            for idx, q in enumerate(questoes):
                with st.container(border=True):
                    st.markdown(f"**Q{idx+1}: {q['pergunta']}**")
                    resp = st.radio(f"Selecione a opção (Q{idx+1}):", 
                                    ["A", "B", "C", "D"], 
                                    key=f"q_{q['id']}",
                                    format_func=lambda x: f"{x}) {q['opcao_'+x.lower()]}")
                    
                    if st.button(f"Confirmar Q{idx+1}"):
                        if resp == q['gabarito']:
                            st.success(f"Correto! {q['referencia']}")
                            st.info(f"💡 Comentário: {q['comentario_ia']}")
                        else:
                            st.error(f"Incorreto. O gabarito é {q['gabarito']}.")
