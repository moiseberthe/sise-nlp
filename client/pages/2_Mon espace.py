import streamlit as st
from controller.dbcontroller import *
import requests
from datetime import datetime

tab1, tab2 = st.tabs(["matcher mon CV", "Filtrage avancé"])

root="localhost" #"nlp-server"

with tab1:
    st.subheader("CV")
    with st.expander("une petite explication"):
        st.write("matche de votre CV avec les offres que nous avons.")
    uploaded_file = st.file_uploader("téléverser votre CV", accept_multiple_files=False)
    if uploaded_file:
        files = {'file': uploaded_file}
        urls=requests.post(f'http://{root}:8000/match', files=files).json()["urls"]
        st.write("Quelques urls d'offres d'emploi que nous vous proposons:")
        for url in urls:
            st.write(url)


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


