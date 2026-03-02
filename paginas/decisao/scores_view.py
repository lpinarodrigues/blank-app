import streamlit as st

def show():
    st.title("📊 Core Scores | Unidade de Decisão Clínica")
    st.markdown("---")

    area = st.sidebar.radio("Selecione a Especialidade:", 
                           ["Cardiologia (SCA/FA)", "Vascular (TEP/TVP)", "Neurologia (AVC/GCS)", "Emergências (Sepse/TGI)"])

    # ... (Manter Cardio, Vascular e Emergências)
    if area == "Cardiologia (SCA/FA)":
        score = st.selectbox("Escolha o Protocolo:", ["HEART Score", "CHA2DS2-VASc", "HAS-BLED"])
        if score == "HEART Score":
            h = st.select_slider("H - História:", options=[0, 1, 2]); e = st.select_slider("E - ECG:", options=[0, 1, 2]); a = st.select_slider("A - Idade:", options=[0, 1, 2]); r = st.select_slider("R - Fatores de Risco:", options=[0, 1, 2]); t = st.select_slider("T - Troponina:", options=[0, 1, 2])
            st.metric("Total", f"{h+e+a+r+t} pts")
        elif score == "CHA2DS2-VASc":
            c = st.checkbox("C - IC"); h = st.checkbox("H - HAS"); idade = st.number_input("Idade:", 18, 110, 65); d = st.checkbox("D - DM"); s = st.checkbox("S2 - AVC"); v = st.checkbox("V - Vasc"); sexo = st.selectbox("Sexo:", ["M", "F"])
            pts = sum([c, h, d, s*2, v]); pts += 2 if idade >= 75 else 1 if idade >= 65 else 0; pts += 1 if sexo == "F" else 0
            st.metric("Total", f"{pts} pts")
        elif score == "HAS-BLED":
            h_b=st.checkbox("H"); a_r=st.checkbox("A-Renal"); a_h=st.checkbox("A-Hep"); s_b=st.checkbox("S"); b_b=st.checkbox("B"); l_b=st.checkbox("L"); e_b=st.checkbox("E"); d_d=st.checkbox("D-Droga"); d_a=st.checkbox("D-Alc")
            st.metric("Total", f"{sum([h_b, a_r, a_h, s_b, b_b, l_b, e_b, d_d, d_a])} pts")

    elif area == "Vascular (TEP/TVP)":
        protocolo = st.selectbox("Escolha:", ["Wells para TEP", "PERC Rule"])
        if protocolo == "Wells para TEP":
            s1=st.checkbox("TVP (+3)"); s2=st.checkbox("TEP Provável (+3)"); s3=st.checkbox("FC > 100 (+1.5)"); s4=st.checkbox("Cirurgia (+1.5)"); s5=st.checkbox("Prévio (+1.5)"); s6=st.checkbox("Hemoptise (+1)"); s7=st.checkbox("Câncer (+1)")
            st.metric("Total", f"{sum([s1*3, s2*3, s3*1.5, s4*1.5, s5*1.5, s6, s7])} pts")
        elif protocolo == "PERC Rule":
            p = [st.checkbox("Idade >= 50"), st.checkbox("FC >= 100"), st.checkbox("SatO2 < 95%"), st.checkbox("Edema MI"), st.checkbox("Hemoptise"), st.checkbox("Cirurgia"), st.checkbox("Prévio"), st.checkbox("Estrogênio")]
            if not any(p): st.success("✅ PERC NEGATIVO")

    elif area == "Neurologia (AVC/GCS)":
        st.header("🧠 Neurologia de Emergência")
        score_neuro = st.selectbox("Selecione o Protocolo:", ["NIHSS (Escala de AVC)", "Escala de Glasgow", "ABCD² Score"])

        if score_neuro == "NIHSS (Escala de AVC)":
            st.markdown("### 🧠 Racional: NIH Stroke Scale")
            st.info("**Para que usar?** Avaliar quantitativamente o déficit neurológico no AVC Isquêmico. Fundamental para indicação de Trombólise e monitorização.")
            st.warning("⚠️ **Dica:** No NIHSS, pontuar o que o paciente **faz**, não o que você acha que ele consegue fazer.")

            # Itens do NIHSS
            c1 = st.selectbox("1a. Nível de Consciência:", [0, 1, 2, 3], format_func=lambda x: {0:"0-Alerta", 1:"1-Sonolento", 2:"2-Estuporoso", 3:"3-Coma"}[x])
            c2 = st.selectbox("1b. Perguntas (Mês/Idade):", [0, 1, 2], format_func=lambda x: {0:"0-Acerta ambas", 1:"1-Acerta uma", 2:"2-Erra ambas"}[x])
            c3 = st.selectbox("1c. Comandos (Abrir/Fechar olhos):", [0, 1, 2], format_func=lambda x: {0:"0-Faz ambos", 1:"1-Faz um", 2:"2-Não faz"}[x])
            c4 = st.selectbox("2. Olhar Conjugado:", [0, 1, 2], format_func=lambda x: {0:"0-Normal", 1:"1-Paralisia parcial", 2:"2-Desvio forçado"}[x])
            c5 = st.selectbox("3. Campos Visuais:", [0, 1, 2, 3], format_func=lambda x: {0:"0-Normal", 1:"1-Hemianopsia parcial", 2:"2-Hemianopsia completa", 3:"3-Cegueira/Bilateral"}[x])
            c6 = st.selectbox("4. Paralisia Facial:", [0, 1, 2, 3], format_func=lambda x: {0:"0-Normal", 1:"1-Apagamento sulco nasogeniano", 2:"2-Paralisia parcial", 3:"3-Paralisia completa"}[x])
            
            st.markdown("#### Força Motora (Membros)")
            colA, colB = st.columns(2)
            m1 = colA.selectbox("5. Braço Esq:", [0, 1, 2, 3, 4], format_func=lambda x: {0:"0-Sem queda", 1:"1-Queda < 10s", 2:"2-Algum esforço contra gravidade", 3:"3-Sem esforço contra gravidade", 4:"4-Sem movimento"}[x])
            m2 = colB.selectbox("5. Braço Dir:", [0, 1, 2, 3, 4])
            m3 = colA.selectbox("6. Perna Esq:", [0, 1, 2, 3, 4], format_func=lambda x: {0:"0-Sem queda", 1:"1-Queda < 5s", 2:"2-Algum esforço", 3:"3-Sem esforço", 4:"4-Sem movimento"}[x])
            m4 = colB.selectbox("6. Perna Dir:", [0, 1, 2, 3, 4])

            c7 = st.selectbox("7. Ataxia Apendicular:", [0, 1, 2], format_func=lambda x: {0:"0-Ausente", 1:"1-Presente em 1 membro", 2:"2-Presente em 2 membros"}[x])
            c8 = st.selectbox("8. Sensibilidade:", [0, 1, 2], format_func=lambda x: {0:"0-Normal", 1:"1-Perda leve/moderada", 2:"2-Perda grave"}[x])
            c9 = st.selectbox("9. Linguagem (Afasia):", [0, 1, 2, 3], format_func=lambda x: {0:"0-Normal", 1:"1-Afasia leve/mod", 2:"2-Afasia grave", 3:"3-Global/Mutismo"}[x])
            c10 = st.selectbox("10. Disartria:", [0, 1, 2], format_func=lambda x: {0:"0-Normal", 1:"1-Leve/Mod", 2:"2-Grave"}[x])
            c11 = st.selectbox("11. Extinção/Negligência:", [0, 1, 2], format_func=lambda x: {0:"0-Normal", 1:"1-Negligência parcial", 2:"2-Negligência completa"}[x])

            total_nihss = sum([c1, c2, c3, c4, c5, c6, m1, m2, m3, m4, c7, c8, c9, c10, c11])
            st.divider()
            st.metric("Total NIHSS", f"{total_nihss} pts")

            if total_nihss == 0: st.success("Sem déficit neurológico evidente.")
            elif total_nihss < 5: st.info("AVC Leve. Avaliar se o déficit é limitante para indicação de trombólise.")
            elif total_nihss < 15: st.warning("AVC Moderado. Forte indicação de trombólise (dentro da janela).")
            elif total_nihss < 25: st.error("AVC Grave. Risco de transformação hemorrágica aumentado.")
            else: st.error("AVC Muito Grave. Prognóstico reservado.")

        elif score_neuro == "Escala de Glasgow":
            # (Lógica anterior de Glasgow...)
            st.subheader("Glasgow")
            o = st.selectbox("Ocular:", [4,3,2,1]); v = st.selectbox("Verbal:", [5,4,3,2,1]); m = st.selectbox("Motora:", [6,5,4,3,2,1])
            st.metric("Total", f"{o+v+m} pts")

    elif area == "Emergências (Sepse/TGI)":
        # (Lógica de qSOFA e HDA...)
        st.header("🚨 Emergências Clínicas")
        score_em = st.selectbox("Selecione:", ["qSOFA (Sepse)", "Glasgow-Blatchford (HDA)"])
        if score_em == "qSOFA (Sepse)":
            f = st.checkbox("FR >= 22"); g = st.checkbox("GCS < 15"); p = st.checkbox("PAS <= 100")
            st.metric("Total qSOFA", f"{sum([f, g, p])} pts")
