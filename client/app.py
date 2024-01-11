

import streamlit as st
from controller.dbcontroller import *
import pandas as pd
import requests
import matplotlib.pyplot as plt 
from wordcloud import WordCloud
import seaborn as sn
import numpy as np
import plotly.express as px

root="localhost" #"nlp-server"

#offres
try:
    offres   = requests.get(f'http://{root}:8000/annonces').json()
    n_offres = len(offres) 
except:
    n_offres= 0

#villes
try:
    villes   = requests.get(f'http://{root}:8000/cities/?offset=0&limit=4000').json()
    n_villes = len(villes)
except:
    n_villes= 0

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
# st.write("Les filtres: ")
# mois = st.slider('Mois concernés', 1, 31, (1, 31))
# options = st.multiselect('types de contrat', contrats)

cities = requests.get(f'http://{root}:8000/cities/?offset=0&limit=4000')
cities = cities.json()
df = pd.DataFrame(cities)
df['count'] = df['count'] * 100

st.map(df,
    latitude='gps_lat',
    longitude='gps_lng',
    size='count'
)


st.write("")
st.write("")

st.header("Nuage de mots de notre corpus")
with st.expander("petite explication"):
    st.write("(il s'agit de mots du corpus nettoyé avec nltk et racinisé)")

wordc= requests.get(f'http://{root}:8000/sentences').json()
wordcloud = WordCloud().generate(" ".join(wordc["res"]))
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)


st.write("")
st.write("")

st.header("Répartition de nos documents")
with st.expander("petite explication"):
    st.write("(tsne des documents reparti sur 2 composants et coloré par leurs clusters d'appartenance (kmeans sur 10 classes))")

tsne=requests.get(f'http://{root}:8000/tsne').json()["tsne"]
clusters=requests.get(f'http://{root}:8000/clustering').json()["clust"]
tsne= np.array(tsne)

#fig, ax = plt.subplots()

# fig2 = sn.scatterplot(x= tsne[:, 0], y= tsne[:, 1], hue=clusters)
# for i in range(len(tsne[:,0])):
#     plt.text(x= tsne[i, 0], y= tsne[i, 1], s=i)
# st.pyplot(fig2.get_figure())

st.write("dataframe des documents avec composants tsne et groupes d'appartenance")

df1= pd.DataFrame(tsne, columns=["composant0", "composant1", "composant2"])
df1["cluster"]= clusters
st.write(df1)


st.write("")
st.write("")
st.write("affichage des documents sur un graphe")

tab1, tab2 = st.tabs(["plotly (3D)", "matplotlib 3D plot"])

with tab1:
    fig = px.scatter_3d(df1, x="composant0", y="composant1", z='composant2', color='cluster', opacity=0.7)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


with tab2:       
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection="3d")
    graph = ax.scatter(tsne[:, 0], tsne[:, 1], tsne[:, 2], s=50, c=clusters)
    ax.set_xlabel("composant0")
    ax.set_ylabel("composant1")
    ax.set_zlabel("composant2")
    for i in range(len(tsne[:,0])):
        ax.text(x= tsne[i, 0], y= tsne[i, 1], z=tsne[i, 2], s=i)
    ax.view_init(60, 80) 
    st.pyplot(fig)
    


