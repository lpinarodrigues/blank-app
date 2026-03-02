import streamlit as st
from paginas.pharma import antibioticos, vasoativas, cardio, seguranca

def show():
    st.title("💊 Core Pharma | Inteligência Farmacológica")
    st.markdown("---")

    menu = st.sidebar.radio("Navegação Pharma:", 
                           ["Antibióticos & Renal", "Drogas Vasoativas & SRI", "Cardio Pharma", "Interações & Segurança"],
                           key="pharma_menu_radio")

    if menu == "Antibióticos & Renal":
        antibioticos.show()
    elif menu == "Drogas Vasoativas & SRI":
        vasoativas.show()
    elif menu == "Cardio Pharma":
        cardio.show()
    elif menu == "Interações & Segurança":
        seguranca.show()
