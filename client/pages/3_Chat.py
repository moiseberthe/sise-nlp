

import streamlit as st
import random
import time
import requests

prompts= []

root="localhost" #"nlp-server"

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("how can we help you?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    rep= requests.post(f'http://{root}:8000/chat', json={"text": prompt}).json()
    #sentiment= requests.post(f'http://{root}:8000/sentiment', json={"text": prompt}).json()
    #print(sentiment)
    #get answer
    answer= "urls qui matchent le mieux avec votre requête: \n"+ rep["url"]
    st.session_state.messages.append({"role": "assistant", "content": answer})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"]=="assistant": 
            message_placeholder = st.empty()
            full_response = ""
            for chunk in message["content"].split():
                full_response += chunk + " "
                time.sleep(0.02)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
        else:
            st.markdown(message["content"])


