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

col1, col2, col3 = st.columns(3)

with col1:
    Genre = st.multiselect("quel type de nourriture ? ", [
        'Pizza', 'Grillades', 'Poissons', 'Tapas', 'Burger', 'Fruit de Mer',
        'Fondues'
    ])
    st.write("You selected", len(Genre), 'Genre')
with col2:
    hobby = st.selectbox("Langues parlées: ",
                         ['Français', 'Anglais', 'Allemand', 'Espagnol'])
    st.write("The language is: ", hobby)

with col3:
    hobby = st.selectbox("Ambiance: ",
                         ['Cosie', 'Festive', 'Date', 'Underground'])
    st.write("L'ambiance est : ", hobby)


@st.cache(hash_funcs={folium.folium.Map: lambda _: None},
          allow_output_mutation=True)
def make_map(field_to_color_by):
    main_map = folium.Map(location=(45.853, 2.35), zoom_start=1)
