import streamlit as st
import time
from controller.dbcontroller import *

from datetime import datetime



st.subheader("Listes des offres")

if st.button('rafraichir la liste'):
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hip!')
    time.sleep(.5)
    st.toast('Hooray!', icon='🎉')
