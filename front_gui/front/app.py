import pandas as pd
import base64
import streamlit as st
import numpy as np
import altair as alt
#from streamlit_folium import folium_static
import folium
from branca.colormap import linear, LinearColormap
from geopy.geocoders import Nominatim
import streamlit as st
import geocoder

# voir cette histoire de cache pour que ca aille plus vite ?

st.set_page_config(
        page_title="Landing Page", # => Quick reference - Streamlit
        page_icon="🐍",
        layout="centered", # wide
        initial_sidebar_state="auto") # collapsed


#boite sélectiion multiple plusieurs params en même temps
Genre = st.multiselect("Genre ",
                         ['Italien', 'Français', 'Iranien'])

st.write("You selected", len(Genre), 'Genre')

#boite sélection un seul param

hobby = st.selectbox("Hobbies: ",
                     ['Dancing', 'Reading', 'Sports'])
st.write("Your hobby is: ", hobby)

""" image_path = 'image_path = 'images/python.png''


def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded


def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="test.jpg;base64,{encoded}">'
    return tag


st.markdown(f'<img src="test.jpg",width = "1000",height="1000", unsafe_allow_html=True>')
st.write(f'{image_tag(image_path)}</a>',
         unsafe_allow_html=True)
 """

st.write(f"<img src='test.jpg',width = '1000',height='1000'>")

if st.checkbox('Show progress bar'):
    import time

    "quand on fera tourner le code / voir si on peut lancer avec le cache ?"
    "fonction echo display code et permet de le run ?"

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')

@st.cache
def get_map_data():

    return pd.DataFrame(np.random.randn(1000, 2) + [45.853, 2.35],
                        columns=['lat', 'lon'])


df = get_map_data()

st.map(df)

#col method = Container

import streamlit as st
import pytz
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import folium
import os
from streamlit_folium import folium_static
'''
# TaxiFareModel front
'''

#date_time

date = st.date_input('Date', datetime.date(datetime.now()))
time = st.time_input('Time', datetime.time(datetime.now()))
date_time = f'{date} {time}'

#nbr passager
nbr_passenger = list(range(1, 9))

option = st.selectbox('Select number of passenger',nbr_passenger)

#pickup
pickup_longitude  = st.number_input('pickup_longitude')
pickup_latitude = st.number_input('pickup_latitude')

#dropoff
dropoff_longitude = st.number_input('dropoff_longitude')

dropoff_latitude = st.number_input('dropoff_latitude')

#maps
def path(pickup_longitude, pickup_latitude,dropoff_longitude, dropoff_latitude):
    return pd.DataFrame([[pickup_longitude, pickup_latitude], [dropoff_longitude, dropoff_latitude]],
    columns=['lat', 'lon'])

df = path(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)

m = folium.Map(location=[df['lat'][0], df['lon'][0]], zoom_start=4)

points = [(df['lat'][0], df['lon'][0]),(df['lat'][1], df['lon'][1]) ]
folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

folium.Marker(location=[df['lat'][1], df['lon'][1]],
              icon=folium.Icon(color="red")).add_to(m)
folium.Marker(
    location=[df['lat'][0], df['lon'][0]],
    icon=folium.Icon(color="red")
).add_to(m)
geojson_path = os.path.join( "departements.json")
folium_static(m)
#call API

if st.button('Validate'):
    url = 'https://taxifare.lewagon.ai/predict?'
    params = {
        'pickup_datetime': date_time,
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': nbr_passenger
    }
    pred = requests.get(url, params =params).json()
    st.write('Price', round(pred['prediction'],2))

# test (48.85737141173452, 2.352283194721945)
