

import streamlit as st
import time
import requests
from env import server_url

prompts= []

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("how can we help you?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    rep= requests.post(f'http://{server_url}/chat', json={"text": prompt}).json()
    #get answer
    answer= rep["url"]
    sentiment= requests.post(f'http://{server_url}/sentiment', json={"text": prompt}).json()["sentiment"]
    if sentiment in ["red" , "tomato"]:
        st.toast('attention à ce que vous écrivez!!!', icon='😠')
        st.session_state.messages.append({"role": "assistant", "content": ["veuillez saisir des trucs moins insultants s'il vous plait"]})
    elif sentiment == "green":
        st.toast('Trop de positivité dans vos écris!!!', icon='😊')
        st.session_state.messages.append({"role": "assistant", "content": answer})
    elif sentiment == "white":
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.toast('un sentiment assez neutre dans vos écris!!!', icon='😐')
    

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"]=="user": 
            message_placeholder = st.empty()
            full_response = ""
            for chunk in message["content"].split():
                full_response += chunk + " "
                time.sleep(0.02)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
        else:
            if len(message["content"])!=1:
                st.write("urls qui matchent le mieux avec votre requête: ")
            for url in message["content"]:
                st.write(url)


