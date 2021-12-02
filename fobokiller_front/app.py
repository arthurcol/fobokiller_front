#from io import UnsupportedOperation
#from logging import PlaceHolder
import pandas as pd
import numpy as np
#import base64
import streamlit as st
import altair as alt
import folium
import requests
import os
import folium
from streamlit_folium import folium_static

#import  csv
lasagna_req = pd.read_csv("gs://fobokiller-722/data/lasagnas.csv",
                          index_col=0).sort_values('metric sim_ratio',
                                                   ascending=False)
french_req = pd.read_csv("gs://fobokiller-722/data/french_food.csv",
                         index_col=0).sort_values('metric sim_ratio',
                                                  ascending=False)
music_req = pd.read_csv("gs://fobokiller-722/data/music.csv",
                        index_col=0).sort_values('metric sim_ratio',
                                                 ascending=False)
pizza_req = pd.read_csv("gs://fobokiller-722/data/pizza.csv",
                        index_col=0).sort_values('metric sim_ratio',
                                                 ascending=False)
surprise_req = pd.read_csv("gs://fobokiller-722/data/Surprise_me!.csv",
                           index_col=0).sort_values('metric sim_ratio',
                                                    ascending=False)
#URL API
url_details_base = 'https://api9-2rnijzpfva-ew.a.run.app/details?alias='
url_api_rate = 'https://api9-2rnijzpfva-ew.a.run.app/summary_reviews?'
url_api = 'https://api9-2rnijzpfva-ew.a.run.app/summary_reviews2?'


st.set_page_config(
    page_title="FOBO Kiler",  # => Quick reference - Streamlit
    page_icon="🍖",
    layout="wide",  # wide
    initial_sidebar_state="auto")  # collapsed


st.markdown(
    '''<h1 style="text-align:center;
    font-size:100px;font-family:Gill Sans, sans-serif;">
    🍗 FOBO Killer ! 🍗</h1>''',
    unsafe_allow_html=True)
m = folium.Map(location=[48.85584630805084, 2.3452032500919433],
               zoom_start=12,
               position='')

st.markdown("""<br/><br/><br/>""", unsafe_allow_html=True)

st.markdown(
    """<p style="font-size:23px;margin-bottom:-100px">
    What do you want to eat today ? 😋</p>""",
    unsafe_allow_html=True)
query_food = st.text_input(placeholder="I would like to eat a vegie burger in a cosy place",
                           label='')
st.markdown("""<br/><br/>""", unsafe_allow_html=True)
st.markdown('<p style="font-size:23px;">How <big>FOBO</big>ic are you ?</p>',
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
    #with st.spinner(text='Looking for the best restaurant for you...'):

    #init map
    m = folium.Map(location=[48.85584630805084, 2.3452032500919433],
                   zoom_start=12, position='')

    #get lat and long of restaurants
    #request api
    params={'text':query_food,
            'n_best':nb,
            'min_review':10}

    #df de base + get aliases for second request
    #result_reviews = requests.get(url_api, params=params).json()
    #result_reviews_df = pd.DataFrame(result_reviews)
    #aliases = list(result_reviews_df['review_clean'].keys())
    #get the rate_filtered
    rate = requests.get(url_api_rate, params=params).json()
    df_rate = pd.DataFrame(rate)
    st.write(df_rate)
    aliases = list(df_rate['reviews'].keys())

    #request second api
    url_details=url_details_base+'&alias='.join(aliases)

    details = requests.get(url_details + '&alias='.join(aliases)).json()
    details_df = pd.DataFrame(details)
    details_df.set_index('alias', inplace=True)

    #create big df
    result_df = details_df.join(
        df_rate).sort_values('metric sim_ratio', ascending=False)
    if query_food == 'I want to eat lasagnas without meat':
        for alias in lasagna_req.index:
            folium.Marker(location=[
            result_df['latitude'][alias], result_df['longitude'][alias]
            ],
                      icon=folium.Icon(color="blue",
                                       icon='mapmarker',
                                       angle=30),
                      popup=folium.Popup(html=f"""
                                    <body>
                                    <div id="title">
                                        <h3>{lasagna_req['name'][alias]}</h3>
                                    </div>

                                    <div id="col">
                                        <p style=
                                        "color:#191970;
                                        font-size: 20px;
                                        border-right:0px;
                                        text-align:left;
                                        ">{round(lasagna_req['rate_filtered'][alias],1)}/5</p>
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
    if query_food == "I don't know what to eat but I feel like having something original. Surprise me!":

        for alias in surprise_req.index:
            folium.Marker(location=[
            result_df['latitude'][alias], result_df['longitude'][alias]
            ],
                      icon=folium.Icon(color="blue",
                                       icon='mapmarker',
                                       angle=30),
                      popup=folium.Popup(html=f"""
                                    <body>
                                    <div id="title">
                                        <h3>{surprise_req['name'][alias]}</h3>
                                    </div>

                                    <div id="col">
                                        <p style=
                                        "color:#191970;
                                        font-size: 20px;
                                        border-right:0px;
                                        text-align:left;
                                        ">{round(surprise_req['rate_filtered'][alias],1)}/5</p>
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
    if query_food == 'I would like a good pizza but I am allergic to gluten':
        for alias in pizza_req.index:
            folium.Marker(location=[
            result_df['latitude'][alias], result_df['longitude'][alias]
            ],
                      icon=folium.Icon(color="blue",
                                       icon='mapmarker',
                                       angle=30),
                      popup=folium.Popup(html=f"""
                                    <body>
                                    <div id="title">
                                        <h3>{pizza_req['name'][alias]}</h3>
                                    </div>

                                    <div id="col">
                                        <p style=
                                        "color:#191970;
                                        font-size: 20px;
                                        border-right:0px;
                                        text-align:left;
                                        ">{round(pizza_req['rate_filtered'][alias],1)}/5</p>
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
    if query_food == 'I am visiting paris and I want to eat good french food, in an authentic place but not with many people':
        for alias in french_req.index:
            folium.Marker(location=[
            result_df['latitude'][alias], result_df['longitude'][alias]
            ],
                      icon=folium.Icon(color="blue",
                                       icon='mapmarker',
                                       angle=30),
                      popup=folium.Popup(html=f"""
                                    <body>
                                    <div id="title">
                                        <h3>{french_req['name'][alias]}</h3>
                                    </div>

                                    <div id="col">
                                        <p style=
                                        "color:#191970;
                                        font-size: 20px;
                                        border-right:0px;
                                        text-align:left;
                                        ">{round(french_req['rate_filtered'][alias],1)}/5</p>
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
    if query_food == 'I want to eat a traditional french meal with music':
        for alias in music_req.index:
            folium.Marker(location=[
            result_df['latitude'][alias], result_df['longitude'][alias]
            ],
                      icon=folium.Icon(color="blue",
                                       icon='mapmarker',
                                       angle=30),
                      popup=folium.Popup(html=f"""
                                    <body>
                                    <div id="title">
                                        <h3>{music_req['name'][alias]}</h3>
                                    </div>

                                    <div id="col">
                                        <p style=
                                        "color:#191970;
                                        font-size: 20px;
                                        border-right:0px;
                                        text-align:left;
                                        ">{round(music_req['rate_filtered'][alias],1)}/5</p>
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
                    Where you can enjoy your meal ! 🤤 </h3> """,
                unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    #display maps and res


    col = st.columns((2, 1, 2))
    for i in range(nb):
        if query_food == 'I want to eat lasagnas without meat':
            direction = st.radio('Restaurant', (lasagna_req.index))
            with col[0]:
                if direction == lasagna_req.index[i]:
                    st.markdown(f"""{lasagna_req["reviews_heatmaps_html"][i]}""",
                    unsafe_allow_html=True)
            col[1].markdown(
            f"""<progress id="file" max="0.5" value="{lasagna_req['metric sim_ratio'][i]}" style="margin-right:0px"></progress><br/><br/><br/>""",
            unsafe_allow_html=True)


        if query_food == "I don't know what to eat but I feel like having something original. Surprise me!":
            with col[0]:
                direction = st.radio('Restaurant', (surprise_req.index))
                if direction == surprise_req.index[i]:

                    st.markdown(f"""{surprise_req["reviews_heatmaps_html"][i]}""",
                    unsafe_allow_html=True)
            col[1].markdown(
                f"""<progress id="file" max="0.5" value="{surprise_req['metric sim_ratio'][i]}" style="margin-right:0px"></progress><br/><br/><br/>""",
                unsafe_allow_html=True)


        if query_food == 'I want to eat a traditional french meal with music':
            direction = st.radio('Restaurant', (music_req.index))
            with col[0]:
                if direction == music_req.index[i]:
                    st.markdown(f"""{music_req["reviews_heatmaps_html"][i]}""",
                    unsafe_allow_html=True)
            col[1].markdown(
                f"""<progress id="file" max="0.5" value="{music_req['metric sim_ratio'][i]}" style="margin-right:0px"></progress><br/><br/><br/>""",
                unsafe_allow_html=True)


        if query_food == 'I am visiting paris and I want to eat good french food, in an authentic place but not with many people':
            with col[0]:
                direction = st.radio('Restaurant', (french_req.index))
                if direction == french_req.index[i]:
                    st.markdown(
                        f"""{french_req["reviews_heatmaps_html"][i]}""",
                        unsafe_allow_html=True)
            col[1].markdown(
                f"""<progress id="file" max="0.5" value="{french_req['metric sim_ratio'][i]}" style="margin-right:0px"></progress><br/><br/><br/>""",
                unsafe_allow_html=True)


        if query_food == 'I would like a good pizza but I am allergic to gluten':
            with col[0]:
                direction = st.radio('Restaurant', (pizza_req.index))
                if direction == pizza_req.index[i]:
                    st.markdown(f"""{pizza_req["reviews_heatmaps_html"][i]}""",
                    unsafe_allow_html=True)
            col[1].markdown(
            f"""<progress id="file" max="0.5" value="{pizza_req['metric sim_ratio'][i]}" style="margin-right:0px"></progress><br/><br/><br/>""",
            unsafe_allow_html=True)

    with col[2]:
        folium_static(m, width=700, height=400)



    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown(f"""<h3 style="text-align:center;
                        font-family:Baskerville, Baskerville Old Face, Garamond, Times New Roman, sans-serif">
                        Why you have to go !!!</h3><br/> """, unsafe_allow_html=True)
