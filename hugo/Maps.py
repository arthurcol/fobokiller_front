import pandas as pd
import numpy as np
import base64
import streamlit as st
import altair as alt
import folium
from branca.colormap import linear, LinearColormap
#from geopy.geocoders import Nominatim
import requests
import time
import os
import folium
from streamlit_folium import folium_static

#importing csv file
path = os.path.join(os.path.dirname(__file__), 'data/final_resto_list.csv')
df = pd.read_csv(path, index_col=0)

#creating unique categories list
liste_cat = list(df['categories'].str.split(', ', expand=False))
cat = set([item for sublist in liste_cat for item in sublist])
categories = [c.capitalize().replace('_', ' ') for c in list(cat)]

#creating price_range dict
price_range = {'€': 1, '€€': 2, '€€€': 3, '€€€€': 4}


#creating arrondissement dict
def selector(k):
    if k == 1 | k == 11:
        return 'st'
    if k == 2 | k == 12:
        return 'nd'
    if k == 3 | k == 13:
        return 'rd'
    return 'st'


arrondissements = {str(k) + selector(k): 75000 + k for k in range(1, 21)}

#URL API
url_api = 'https://api3-2rnijzpfva-ew.a.run.app/detail?'

st.set_page_config(
    page_title="FOBO Kiler",  # => Quick reference - Streamlit
    page_icon="🍖",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

st.title('FOBO Killer !')

query_food = st.text_input(
    'What do you want to eat today ? 😋',
    value='Miam',
)
query_location = st.text_input('Where are you ? 🧐')

expander = st.expander('Optional filters')

with expander:

    filters = st.columns(3)
    cat_select = filters[0].multiselect('Choose a category', categories)
    arrondissement_string = filters[1].multiselect('Arrondissement',
                                                   arrondissements)
    price_symbol = filters[2].multiselect('Price range',
                                          ['€', '€€', '€€€', '€€€€'])

st.write('### How _FOBOic_ are you ?')
foboic = st.columns(3)
foboic[0].write('BIG TIME')
foboic[1].write('Taking my pills...')
foboic[2].write('I\'m ok !')
nb = st.slider('', 1, 20)

if st.button('Surprise me!'):
    with st.spinner(text='Looking for the best restaurant for you...'):
        st.success('Bon appetit!')

        #init map
        m = folium.Map(location=[48.86489231778049, 2.3799136342856975],
                       zoom_start=12)

        #get lat and long of restaurants
        #request api
        params = {'alias': 'le-comptoir-de-la-gastronomie-paris'}
        resultat = pd.DataFrame(requests.get(url_api, params=params).json())
        for i in range(len(resultat)):
            folium.Marker(
                location=[resultat['latitude'][i], resultat['longitude'][i]],
                icon=folium.Icon(color="blue", icon='mapmarker',
                                 angle=30)).add_to(m)

        #localisation où suis-je ?
        folium.Marker(location=[48.86489231778049, 2.3799136342856975],
                      icon=folium.Icon(color="red", icon='user')).add_to(m)

        #display map
        folium_static(m)
