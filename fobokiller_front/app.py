from io import UnsupportedOperation
from logging import PlaceHolder
import pandas as pd
import numpy as np
import base64
import streamlit as st
import altair as alt
import folium
import requests
import os
import folium
from streamlit_folium import folium_static

#URL API
url_details_base = 'https://api10-2rnijzpfva-ew.a.run.app/details?alias='
url_api_rate = 'https://api10-2rnijzpfva-ew.a.run.app/summary_reviews?'
url_api = 'https://api10-2rnijzpfva-ew.a.run.app/summary_reviews2?'


st.set_page_config(
    page_title="FOBO Kiler",  # => Quick reference - Streamlit
    page_icon="🍖",
    layout="wide",  # wide
    initial_sidebar_state="auto")  # collapsed

st.markdown(
    '''<h1 style="text-align:center;
    font-size:100px;font-family:Gill Sans, sans-serif;">
    🍗 FOBO Killer ! 🍗</h1><br/><br/>''',
    unsafe_allow_html=True)
m = folium.Map(location=[48.85584630805084, 2.3452032500919433],
               zoom_start=12,
               position='')

st.markdown(
    """<p style="font-size:23px;margin-bottom:-100px;">
    What do you want to eat today ? 😋</p>""",
    unsafe_allow_html=True)
query_food = st.text_input(placeholder="I would like to eat burger ...",
                           label='')
st.markdown("""<br/><br/>""", unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:23px;margin-bottom:-10px;">How <big>FOBO</big>ic are you ?</p>',
    unsafe_allow_html=True)
nb = 12 - st.slider('', 10, 2, value = 5)
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
                    zoom_start=12, position='')

        #get lat and long of restaurants
        #request api
        params={'text':query_food,
                'n_best':nb,
                'min_review':10}

        #df de base + get aliases for second request
        result_reviews = requests.get(url_api, params=params).json()
        result_reviews_df = pd.DataFrame(result_reviews)
        aliases = list(result_reviews_df['review_clean'].keys())


        #request second api
        url_details=url_details_base+'&alias='.join(aliases)

        details = requests.get(url_details + '&alias='.join(aliases)).json()
        details_df = pd.DataFrame(details)
        details_df.set_index('alias', inplace=True)

        #create big df
        result_df = details_df.join(result_reviews_df).sort_values(
            'metric sim_ratio', ascending=False)

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
                                            ">{round(result_df['rate_filtered_y'][alias],1)}/5</p>
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


        st.markdown("""<h3 style="text-align:center;
                        font-family:Baskerville, Baskerville Old Face, Garamond, Times New Roman, sans-serif">
                        Where you can enjoy your meal ! 🤤 </h3><br/> """,
                    unsafe_allow_html=True)


        #display maps and res
        #list_restau = result_df.index
        #direction = st.radio('Restaurant', (result_df.index))
        col= st.columns((1,1,2))
        for i in range(nb):
            with col[0]:
                st.markdown(f"<h3>{result_df['name'][i]}</h3>",
                            unsafe_allow_html=True)
            col[1].markdown(
                f"""<meter id="file" max="0.40" low=".25" optimum=".35" value="{result_df['metric sim_ratio'][i]}" style="margin-right:0px; width:170px; height:20px; margin: .8em"></meter>""",
                unsafe_allow_html=True)

            #if direction == result_df.index[i]:

        st.markdown("""<h2 style='text-align:center;
                        font-family:Baskerville, Baskerville Old Face, Garamond, Times New Roman, sans-serif"'> Why you have to go!!!<h2/>""", unsafe_allow_html=True)
        for i in range(nb):
            with st.expander(result_df['name'][i]):
                review_col = list(set(result_df["reviews_heatmaps_html"][i]))


                sentence_heat ='\n - ' + '\n \n - '.join(review_col[:5])
                st.markdown(f"""<br/><br/>{sentence_heat}""", unsafe_allow_html=True)



        with col[2]:
            folium_static(m, width=600, height=400)
