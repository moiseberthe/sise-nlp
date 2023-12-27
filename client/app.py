

import streamlit as st
from controller.dbcontroller import *
import pandas as pd
import numpy as np

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

df = pd.DataFrame({
    "col1": np.random.randn(1000) / 50 + 37.76,
    "col2": np.random.randn(1000) / 50 - 122.4,
    "col3": np.random.randn(1000) * 100,
    "col4": np.random.rand(1000, 4).tolist(),
})

st.map(df,
    latitude='col1',
    longitude='col2',
    size='col3',
    color='col4'
)