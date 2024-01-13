import streamlit as st
import time
from controller.dbcontroller import *
import requests
import pandas as pd
from env import server_url

st.subheader("Listes des offres")

sources = requests.get(f'http://{server_url}/sources/?offset=0&limit=10')
sources = sources.json()

source = st.selectbox(
    'Source',
    tuple([s['name'] for s in sources[:2]]))
nb_annonces = st.number_input('Nombre d\'annonces', min_value= 10, max_value= 400)

if st.button('rafraichir la liste'):
    st.toast('Rafraichissement en cours!')
    time.sleep(.5)
    annonces = requests.get(f'http://{server_url}/annonces/scrape/{source}/{nb_annonces}')
    st.toast('chargement....!')
    time.sleep(.5)
    annonces = annonces.json()
    df = pd.DataFrame(annonces)
    st.dataframe(df)
    st.toast('Liste rafraichie!', icon='🎉')
