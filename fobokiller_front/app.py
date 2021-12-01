from io import UnsupportedOperation
from logging import PlaceHolder
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


#URL API
url_details_base = 'https://api6-2rnijzpfva-ew.a.run.app/details?alias='
url_api = 'https://api6-2rnijzpfva-ew.a.run.app/summary_reviews?'

st.set_page_config(
        page_title="FOBO Kiler", # => Quick reference - Streamlit
        page_icon="🍖",
        layout="centered", # wide
        initial_sidebar_state="auto") # collapsed

st.markdown(
    '<h1 style="text-align:center; font-size:100px;font-family:Gill Sans, sans-serif;">🍗 FOBO Killer ! 🍗</h1>',
    unsafe_allow_html=True)


st.markdown("""<br/><br/><br/>""", unsafe_allow_html=True)
st.markdown(
    """<p style="font-size:23px;margin-bottom:-100px">What do you want to eat today ? 😋</p>""",
    unsafe_allow_html=True)
query_food = st.text_input(placeholder="I would like to eat a vegie burger in a cosy place",
                           label='')
st.markdown("""<br/><br/>""", unsafe_allow_html=True)
st.markdown('<p style="font-size:23px;">How FOBOic are you ?</p>',
            unsafe_allow_html=True)
nb = st.slider('', 2, 10)
st.markdown("""<body>
            <div id="col">
                <p style="font-size:18px;">BIG TIME 😰</p>
                <p style='text-align:right;font-size:18px'>I\'m ok !😎</p>
            </div>
            </body>
            <style>
            #col {
                column-count: 2;
                }</style>""",
            unsafe_allow_html=True)

if st.button('Surprise me!'):
    with st.spinner(text='Looking for the best restaurant for you...'):

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
                result_df['latitude'][alias], result_df['longitude'][alias]
            ],
                          icon=folium.Icon(color="blue",
                                           icon='mapmarker',
                                           angle=30),
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
                                        text-align:left;
                                        ">{result_df['rating'][alias]}/5</p>
                                        <p
                                        style="
                                        font-size:15px;
                                        border-left:0px;

                                        "> {result_df['address'][alias]}.</p>
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
        st.markdown("""<h3 style="text-align:center;
                    font-family:Baskerville, Baskerville Old Face, Garamond, Times New Roman, sans-serif">Where you can enjoy your meal ! 🤤 </h3> """,
                    unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        folium_static(m, width=1440, height=400)

        #st.table(result_df[['nb_sentences', 'nb_review','metric sim_ratio','sentences_pond','metric_pond']])
        metrics_df = result_df.sort_values('metric sim_ratio', ascending=False)

        col1 = [x for x in range(5)]
        col2 = [x for x in range(5)]
        col1 = st.columns(5)
        col2 = st.columns(5)
        #j =0
        #while j < min(5,nb):
        #for k in range(5):
        #   if k <nb:

        #    j+=1
        #if 4<j<nb:
        #while j < min(10,nb):
        #for k in range(5):
        #if k +5 <nb:

        # j+=1
        df_test = pd.DataFrame(
            [['Pizza-Vesuvio', 4.2, '1 rue Gozlin ', .32],
             ['Pizza Julia', 4, '43 rue de Charenton ', 0.2665],
             ['Il Brigante', 4.9, '14 rue Ruisseau ', 0.2809],
             ['Pizza Di Loretta', 4.3, '62 rue Rodier ', .35],
             ['court', 4.6, '14 rue Normandie. ', 0.310],
             ['nom super long pour faire chier', 4.5, '42 rue Tiquetonne.',.17],
             ['O\'Scia', 4.9, '8 rue des Gravilliers.', 0.3159]],
            columns=['name',
                     'rate',
                     'adresse',
                     'metric']).sort_values('metric', ascending=False)

        df_test['metric_adjust'] = df_test['metric']*2.5

        st.markdown("""<h3 style="text-align:center;
                    font-family:Baskerville, Baskerville Old Face, Garamond, Times New Roman, sans-serif">Why you have to go </h3> """,
                    unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        for i in range(nb):
            col1.markdown(
                f"""<span style='font-size:30px;'> {df_test['name'][i]} </span>
                <progress id="file" max="1" value="{df_test['metric_adjust'][i]}" style="margin-right:0px"></progress>
                """,
                unsafe_allow_html=True)
            col2.markdown(
            """'<span style='background-color:rgba(0,79.93747338652611,0,0.6)'> $$$ food but only at a $ price </span><span style=\'background-color:rgba(0,198.37338656187057,0,0.6)\'> will be coming here every time i\'m in paris from now on </span><span style=\'background-color:rgba(0,255.0,0,0.6)\'> mains are  </span><span style=\'background-color:rgba(0,160.61861246824265,0,0.6)\'>€ to € and our wine glasses were  </span><span style=\'background-color:rgba(0,155.39450079202652,0,0.6)\'>€ each (ranging up to or ) </span><span style=\'background-color:rgba(0,57.28849232196808,0,0.6)\'> the absolute fav so far this trip for value </span>'""",unsafe_allow_html=True)
