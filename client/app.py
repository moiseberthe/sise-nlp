

import streamlit as st
from controller.dbcontroller import *
import pandas as pd
import numpy as np
import requests

#offres
offres   = ""
n_offres = 100 

#villes
villes   = ""
n_villes= 10

#type de contrat
contrats= ("cdd", "cdi", "stage", "alternance")


st.header("Overview des Offres")

col1, col2, col3 = st.columns(3)
col1.metric("les offres", n_offres)
col2.metric("les villes", n_villes)
col3.metric("le domaine", "la data")

st.write("")
st.write("")

st.header("Répartition des offres par villes")
#map
st.write("Les filtres: ")
mois = st.slider('Mois concernés', 1, 31, (1, 31))
options = st.multiselect('types de contrat', contrats)

cities = requests.get('http://nlp-server:8000/cities/?offset=0&limit=4000')
cities = cities.json()
df = pd.DataFrame(cities)
df['count'] = df['count'] * 100

st.map(df,
    latitude='gps_lat',
    longitude='gps_lng',
    size='count'
)