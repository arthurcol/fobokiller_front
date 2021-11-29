import base64
import streamlit as st
import altair as alt
from streamlit_folium import folium_static
import folium
from branca.colormap import linear, LinearColormap
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Landing Page",  # => Quick reference - Streamlit
    page_icon="🐍",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed


# 48.86489231778049, 2.3799136342856975 localisation wagon
#def Map
m = folium.Map(location=[48.86489231778049, 2.3799136342856975], zoom_start=12)

#########################
#       df rest         #
#########################

#def lat_long_res(df):

#def lat_long_res(df):
#return pd.DataFrame([[lont_rest[i]], [lat_rest[i]]],
#columns=['lat', 'lon'])


#df_rest = lat_long_res(res)
df_rest = pd.DataFrame([[48.85063269732752,2.337468211852662],
                       [48.86314522468136,2.3005360917738775],
                       [48.887869828496974,2.3431147259766956]],
                       columns = ['lat', 'long'])
for i in range(len(df_rest)):
    folium.Marker(location=[df_rest['lat'][i], df_rest['long'][i]],
                  icon=folium.Icon(color="blue", icon='mapmarker', angle = 30)).add_to(m)
#########################
# localisation du wagon #
#########################


folium.Marker(location=[48.86489231778049, 2.3799136342856975],
              icon=folium.Icon(color="red", icon='user')).add_to(m)




#display map
# a mettre dans le resultat
folium_static(m)
