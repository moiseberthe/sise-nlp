import streamlit as st
import time
from controller.dbcontroller import *

import requests
import pandas as pd



st.subheader("Listes des offres")

sources = requests.get('http://nlp-server:8000/sources/?offset=0&limit=10')
sources = sources.json()

source = st.selectbox(
    'Source',
    tuple([s['name'] for s in sources]))
nb_annonces = st.number_input('Nombre d\'annonces')

if st.button('rafraichir la liste'):
    annonces = requests.get(f'http://nlp-server:8000/jobs/scrape/{source}/{nb_annonces}')
    annonces = annonces.json()
    df = pd.DataFrame(annonces)
    st.dataframe(df)
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hooray!', icon='🎉')
