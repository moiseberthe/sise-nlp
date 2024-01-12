import streamlit as st
from controller.dbcontroller import *
import requests
from datetime import datetime
from streamlit_card import card

tab1, tab2 = st.tabs(["Matcher mon CV", "Filtrage avancé"])

root="localhost" #"nlp-server"

offres = requests.get(f'http://{root}:8000/annonces').json()

if "result" not in st.session_state:
    st.session_state.result = []

with tab1:
    st.subheader("CV")
    with st.expander("une petite explication"):
        st.write("matche de votre CV avec les offres que nous avons.")
    uploaded_file = st.file_uploader("téléverser votre CV", accept_multiple_files=False)
    if uploaded_file:
        files = {'file': uploaded_file}
        urls=requests.post(f'http://{root}:8000/match', files=files).json()["urls"]
        st.write("Les offres qui matchent avec votre CV:")
        for url in urls:
            job= [off for off in offres if off["url"]==url][0]
            cd= card(
                key= job["id"],
                title=job["title"],
                text=["Entreprise: "+job["company_name"], "contrat: "+job["contrat"]["name"], "Lieu: "+job["city"]["name"]],
                #image="https://placekitten.com/500/500",
                url=job["url"],
                styles={
                    "card": {
                        "width": "100%", "height": "300px", "border-radius": "60px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)", "background-color": "white"
                    },
                    "text": {
                        "font-family": "serif"
                    }
                }
            )
            #st.write(url)


with tab2:

    def validate():
        if domaine!="" and emp!="" and typ!="" and comp !="":
            text= domaine+" "+emp+" "+typ+" "+comp 
            rep= requests.post(f'http://{root}:8000/chat', json={"text": text}).json()
            #st.success("")
            st.session_state.result= rep["url"]
        else:
            st.toast("veuillez saisir tous les champs étoilés")
            st.session_state.result= []
            #mess.write("veuillez saisir tous les champs étoilés")
            
    st.header("Filtre")
    with st.form("user_form"):
        mess= st.empty()

        col1, col2 = st.columns(2)

        domaine= col1.text_input("Veuillez saisir un domaine *: ", key = 'w')
        emp= col1.text_input("Veuillez saisir un emplacement géographique *: ", key = 'a')
        typ= col1.selectbox("Veuillez choisir un type de contrat *: ", ("stage", "CDD", "CDI", "alternance"), key = 'b')

        comp= col2.text_input("saisir une liste de compétences *: ", help="html, css, react, ...", key = 'c')
        sal= col2.number_input("Prétention salariale: ", min_value= 400, max_value= 200000, key = 'd')

        st.form_submit_button('Entrer', on_click=validate())

    if len(st.session_state.result) >0:
        for rep in st.session_state.result:
            job= [off for off in offres if off["url"]==rep][0]
            cd= card(
                key= job["id"]*100,
                title=job["title"],
                text=["Entreprise: "+job["company_name"], "contrat: "+job["contrat"]["name"], "Lieu: "+job["city"]["name"]],
                #image="https://placekitten.com/500/500",
                url=job["url"],
                styles={
                    "card": {
                        "width": "100%", "height": "300px", "border-radius": "60px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)", "background-color": "white"
                    },
                    "text": {
                        "font-family": "serif"
                    }
                }
            )

    



