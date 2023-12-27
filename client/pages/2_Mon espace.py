import streamlit as st
from controller.dbcontroller import *

from datetime import datetime

tab1, tab2 = st.tabs(["matcher mon CV", "Filtrage avancé"])

with tab1:
    st.subheader("CV")
    with st.expander("See explanation"):
        st.write("upload your CV to see propositions that match it.")


with tab2:
    def validate():
        form= {}
        print("ok!!")

    #topic modeling here
    st.header("Filtre")
    with st.form("user_form"):
        col1, col2 = st.columns(2)

        domaine= col1.text_input("Veuillez saisir un domaine: ")
        emp= col1.text_input("Veuillez saisir un emplacement géographique: ")
        typ= col1.selectbox("Veuillez choisir un type de contrat: ", ("stage", "CDD", "CDI", "alternance"))

        comp= col2.text_input("saisir une liste de compétences: ", help="html, css, react, ...")
        sal= col2.date_input("Prétention salariale: ")
        password= col2.text_input("Veuillez saisir un mot de passe: ", type="password")

        st.form_submit_button('Entrer', on_click=validate)


