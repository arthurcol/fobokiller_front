import pandas as pd
import numpy as np
import base64
import streamlit as st
import altair as alt
import folium
from branca.colormap import linear, LinearColormap
from geopy.geocoders import Nominatim
import geocoder
import time
import os

#importing csv file
path = os.path.join(os.path.dirname(__file__), 'data/final_resto_list.csv')
df = pd.read_csv(path, index_col=0)

#creating unique categories list
liste_cat = list(df['categories'].str.split(', ', expand=False))
categories = set([item for sublist in liste_cat for item in sublist])

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


st.set_page_config(
        page_title="FOBO Kiler", # => Quick reference - Streamlit
        page_icon="🍖",
        layout="centered", # wide
        initial_sidebar_state="auto") # collapsed



query_food = st.text_input('What do you want to eat today ? 😋',value='Miam',)
query_location = st.text_input('Where are you ? 🧐')

expander = st.expander('Optional filters')

with expander:

    filters = st.columns(3)
    cat_select = filters[0].multiselect('Choose a category',categories)
    arrondissement_string = filters[1].multiselect('Arrondissement',arrondissements)
    price_symbol  = filters[2].multiselect('Price range',['€','€€','€€€','€€€€'])


if st.button('Surprise me!'):
    with st.spinner(text='Looking for the best restaurant for you...'):
        time.sleep(5)
        st.success('Done')



@st.cache
def get_map_data():

    return pd.DataFrame(np.random.randn(1000, 2) + [45.853, 2.35],
                        columns=['lat', 'lon'])


df = get_map_data()

st.map(df)
