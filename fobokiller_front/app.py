import pandas as pd
import numpy as np
import base64
import streamlit as st
import altair as alt
import folium
from branca.colormap import linear, LinearColormap
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
url_details_base = 'https://api6-2rnijzpfva-ew.a.run.app/details?alias='
url_api = 'https://api6-2rnijzpfva-ew.a.run.app/summary_reviews?'

st.set_page_config(
        page_title="FOBO Kiler", # => Quick reference - Streamlit
        page_icon="🍖",
        layout="centered", # wide
        initial_sidebar_state="auto") # collapsed

st.title('FOBO Killer !')

query_food = st.text_input('What do you want to eat today ? 😋',value='Miam',)
query_location = st.text_input('Where are you ? 🧐')

expander = st.expander('Optional filters')

with expander:

    filters = st.columns(3)
    cat_select = filters[0].multiselect('Choose a category',categories)
    arrondissement_string = filters[1].multiselect('Arrondissement',arrondissements)
    price_symbol  = filters[2].multiselect('Price range',['€','€€','€€€','€€€€'])

st.write('### How _FOBOic_ are you ?')
nb = st.slider('', 2, 10)
foboic = st.columns(11)
foboic[0].write('BIG TIME')
foboic[5].write('Taking my pills...')
foboic[10].write('I\'m ok !')

if st.button('Surprise me!'):
    with st.spinner(text='Looking for the best restaurant for you...'):
        st.success('Bon appetit!')

        #init map
        m = folium.Map(location=[48.85584630805084, 2.3452032500919433],
                       zoom_start=12)

        #get lat and long of restaurants
        #request api
        params={'text':query_food,
                'n_best':nb,
                'min_review':10}
        result_reviews = requests.get(url_api, params=params).json()
        result_reviews_df = pd.DataFrame(result_reviews)
        aliases = list(result_reviews_df['reviews'].keys())
        url_details=url_details_base+'&alias='.join(aliases)
        details = requests.get(url_details + '&alias='.join(aliases)).json()
        details_df = pd.DataFrame(details)
        details_df.set_index('alias', inplace=True)
        result_df = details_df.join(result_reviews_df)
        for alias in result_df.index:
            folium.Marker(location=[
                result_df['latitude'][alias], result_df['longitude'][alias]],
                          icon=folium.Icon(color="blue",icon='mapmarker',angle=30),
                          popup=folium.Popup(html=f"""
                                    <body>
                                    <div id="title">
                                        <h3>{result_df['name'][alias]}</h3>
                                    </div>

                                    <div id="col">
                                        <p style=
                                        "color:#191970;
                                        font-size: 20px;
                                        border-right:0px;
                                        ">{result_df['rating'][alias]}/5</p>
                                        <p
                                        style="
                                        font-size:15px;
                                        border-left:0px;
                                        "> Address:</br> {result_df['address'][alias]}.</p>
                                    </div>
                                    </body>
                                    """ + """
                                    <style>
                                    #title {
                                        width=400px;
                                        }
                                    #col {
                                    column-count: 2;
                                    }
                                    </style>""")).add_to(m)

        #localisation où suis-je ?
        folium.Marker(location=[48.86489231778049, 2.3799136342856975],
                    icon=folium.Icon(color="red", icon='user')).add_to(m)

        #display map
        folium_static(m)

        #st.table(result_df[['nb_sentences', 'nb_review','metric sim_ratio','sentences_pond','metric_pond']])
        st.markdown("""<h3>Accuracy score</h3> """, unsafe_allow_html=True)
        metrics_df = result_df.sort_values('metric sim_ratio', ascending=False)


        col1 = [x for x in range(5)]
        col2 = [x for x in range(5)]
        col1 = st.columns(5)
        col2 = st.columns(5)
        j =0
        while j < min(5,nb):
            for k in range(5):
                if k <nb:
                    col1[k].markdown(f"""<h5>{metrics_df['name'][j]}</h5>""",
                                    unsafe_allow_html=True)
                    col1[k].markdown(
                        f"<h5 style='color:#3E3A8F'>{round(metrics_df['metric sim_ratio'][j] * 100, 1)}%</h5>",
                        unsafe_allow_html=True)
                    j+=1
        st.write(j)
        if 4<j<nb:
            while j < min(10,nb):
                for k in range(5):
                    if k +5 <nb:
                        col2[k].markdown(f"""<h5>{metrics_df['name'][j]}</h5>""",
                                        unsafe_allow_html=True)
                        col2[k].markdown(
                            f"<h5 style='color:#3E3A8F'>{round(metrics_df['metric sim_ratio'][j] * 100, 1)}%</h5>",
                            unsafe_allow_html=True)
                    j+=1
