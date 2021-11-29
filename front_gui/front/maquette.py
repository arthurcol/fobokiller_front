import pandas as pd
import base64
import streamlit as st
import numpy as np
import altair as alt
from streamlit_folium import folium_static
import folium
from branca.colormap import linear, LinearColormap
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
from geopy.geocoders import Nominatim

st.write('# Hello, World! We are FOBO solvers ! :sunglasses:')

LOGO_IMAGE = "mondrillan.png"
#mapimage = ...

st.markdown("""
            </div>
            </div>
    <style>
    .container {
        display: flex;
        justify-content: space-evenly;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:30px !important;
        color: #f9a49b !important;
        padding: 35px !important;
    }
    .logo-img {
        float:right;
        height: 600px;
        width: 1800px;
        object-fit: cover;
    }
    </style>
    """,
            unsafe_allow_html=True)
st.markdown(f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
    </div>
    """,
            unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    sentence_input = st.text_input("What kind of restaurant ?")
with col5:
    loc_input = st.text_input("Where are you ?",'Boulevard Sébastopol')
geolocator = Nominatim(user_agent="googlemap")
x=geolocator.geocode(loc_input).point

if st.button('Trouver le restaurant'):
    #url = 'API FOBO killer'
    params = {
        'What do you want to eat': sentence_input,
        'Where are you?': loc_input,
    }

    col1, col2 = st.columns(2)
    with col1:
        st.write(f'You asked for : {sentence_input}')
    with col2:
        st.write(f'You are here : {loc_input} and the geolocation is : {x}')
    #pred = requests.get(url, params =params).json()
    #st.write('Restaurant', (pred['prediction'],...)) #loc des restaus + reviews + ...

LOGO_IMAGE2 = "test.jpg"

st.markdown("""
    <style>
    .container {
        display: flex;
        justify-content: space-evenly;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:18px !important;
        color: #f9a49b !important;
        padding: 35px !important;
    }
    .logo-img {
        float:right;
        height: 300px;
        width: 600px;
        object-fit: cover;
    }
    </style>
    """,
            unsafe_allow_html=True)
st.markdown(f"""
    <div class="container">
        <p class="logo-text">FOBO Killer, c’est une application permettant d’identifier et d’analyser les raisons pour lesquelles un restaurant est plus ou moins bien noté grâce à la puissance du NLP (Natural Language Processing). L’objectif est de recommander le restaurant qui match le plus avec la recherche en mettant en avant ses différentes caractéristiques :pièce_de_viande:
Grâce à FOBO Killer, faire un choix n’aura jamais été aussi simple</p>
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE2, "rb").read()).decode()}">
    </div>
    """,
            unsafe_allow_html=True)
