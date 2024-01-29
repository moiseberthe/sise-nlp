

import streamlit as st
from controller.dbcontroller import *
import pandas as pd
import requests
import matplotlib.pyplot as plt 
from wordcloud import WordCloud
import numpy as np
import plotly.express as px
from env import server_url


st.set_page_config(layout="wide")


defaultOption = {'00': 'Tout'}
filters = []
annonces = requests.get(f'http://{server_url}/annonces').json()
idx = {x['id']:i for i, x in enumerate(annonces)}

cols = st.columns(5)
with cols[0]:
   regions = requests.get(f'http://{server_url}/regions').json()
   choices = {r['id'] : r['name'] for r in regions}
   choices = {**defaultOption, **choices}

   region = st.selectbox(
      "Régions",
      options=list(choices.keys()), format_func=lambda x: choices[x]
   )

with cols[1]:
   if(region == '00'):
      departments = requests.get(f'http://{server_url}/departments').json()
   else:
      departments = requests.get(f'http://{server_url}/regions/{region}').json()['departments']
   
   choices = {row['code'] : row['name'] for row in departments}
   choices = {**defaultOption, **choices}

   department = st.selectbox(
      "Départements",
      options=list(choices.keys()), format_func=lambda x: choices[x]
   )

with cols[2]:
   jobs = requests.get(f'http://{server_url}/jobs').json()
   choices = {row['id'] : row['name'] for row in jobs}
   choices = {**defaultOption, **choices}

   job = st.selectbox(
      "Poste",
      options=list(choices.keys()), format_func=lambda x: choices[x]
   )

with cols[3]:
   contrats = requests.get(f'http://{server_url}/contrats').json()
   choices = {row['id'] : row['name'] for row in contrats}
   choices = {**defaultOption, **choices}
   contract = st.selectbox(
      "Contrats",
      options=list(choices.keys()), format_func=lambda x: choices[x]
   )

with cols[4]:
   activities = requests.get(f'http://{server_url}/activities').json()

   choices = {row['id'] : row['name'] for row in activities}
   choices = {**defaultOption, **choices}

   activity = st.selectbox(
      "Secteur d'activité",
      options=list(choices.keys()), format_func=lambda x: choices[x]
   )

col_names = ['_sa_instance_state', 'url', 'title', 'company_name', 'description',
      'profile', 'activity_id', 'source_id', 'city_id', 'date', 'skills',
      'job_id', 'contrat_id', 'id', 'city', 'departement', 'region',
      'contrat', 'source']

annonces = requests.get(f'http://{server_url}/annonces/{region}/{department}/{job}/{contract}/{activity}').json()
col_names = ['_sa_instance_state', 'url', 'title', 'company_name', 'description',
       'profile', 'activity_id', 'source_id', 'city_id', 'date', 'skills',
       'job_id', 'contrat_id', 'id', 'city', 'gps_lat', 'gps_lng', 'departement', 'region',
       'contrat', 'source']
df_all = pd.DataFrame(annonces, columns=col_names)

sentences = requests.get(f'http://{server_url}/sentences').json()['res']
sentences = np.array(sentences)

doc_indexes = [idx[x['id']] for i, x in df_all.iterrows()]


col1, col2, col3 = st.columns(3)
n_offres = 0
n_city = 0
if (df_all.shape[0] != 0):
   n_offres = df_all.shape[0]
   n_city = df_all['city_id'].unique().shape[0]

col1.metric("les offres", n_offres)
col2.metric("les villes", n_city)
col3.metric("le domaine", "la data")

col01, col02= st.columns(2)
with col01:
    st.text("Nombres d'annonces par type de contrat")
    fig = px.histogram(df_all, x="contrat", nbins=20)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with col02:
    st.text("Nombres d'annonces par source")
    fig = px.histogram(df_all, x="source", nbins=20)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

col01, col02 = st.columns(2)
with col01:
   df_cities = df_all.groupby('city_id').agg(
      {'departement': 'first', 'region': 'first', 'gps_lat': 'first', 'gps_lng': 'first', 'id': 'count'}
   )
   st.text("Nombres d'annonces par ville")
   st.map(df_cities, latitude='gps_lat', longitude='gps_lng', size='id')

with col02:
   if (n_offres > 0):
      st.text("Nuage de mots")
      texts = sentences[doc_indexes]
      wordcloud = WordCloud().generate(" ".join(texts))
      fig, ax = plt.subplots()
      ax.imshow(wordcloud, interpolation='bilinear')
      ax.axis("off")
      st.pyplot(fig)


st.header("Répartition de nos documents")
with st.expander("petite explication"):
    st.write("TSNE des documents reparti sur 2 composants et coloré par leurs clusters d'appartenance (kmeans sur 10 classes)")

tsne = requests.get(f'http://{server_url}/tsne').json()["tsne"]
clusters = requests.get(f'http://{server_url}/clustering').json()["clust"]
tsne= np.array(tsne)

df1 = pd.DataFrame(tsne, columns=["composant0", "composant1", "composant2"])
df1["cluster"]= clusters

st.write("Affichage des documents sur un graphe")

tab1, tab2 = st.tabs(["Plotly (3D)", "Matplotlib 3D plot"])

with tab1:
   fig = px.scatter_3d(df1.iloc[doc_indexes], x="composant0", y="composant1", z='composant2', color='cluster', opacity=0.7)
   fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
   st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab2:       
   fig = plt.figure(figsize=(10, 10))
   ax = plt.axes(projection="3d")
   graph = ax.scatter(tsne[doc_indexes, 0], tsne[doc_indexes, 1], tsne[doc_indexes, 2], s=50, c=df1["cluster"].iloc[doc_indexes])
   ax.set_xlabel("composant0")
   ax.set_ylabel("composant1")
   ax.set_zlabel("composant2")
   for i in range(len(tsne[doc_indexes, 0])):
      ax.text(x= tsne[i, 0], y= tsne[i, 1], z=tsne[i, 2], s=i)
   ax.view_init(60, 80) 
   st.pyplot(fig)