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
st.markdown("""<span style='background-color:rgba(200,147.70981073379517,0,1)'>i forgot this place was vegan until i got there </span>
            <span style='background-color:rgba(200,203.74802505970001,0,1)'> that's what happens when you have a running list of restaurants to visit in paris </span>
            <span style='background-color:rgba(200,255,0,1)'> but seriously, this place is sooo good </span>
            <span style='background-color:rgba(200,110.4891774058342,0,1)'> order l'allume, potatoes wedges and pay an extra euro for a beer </span>""",unsafe_allow_html=True)

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
                                        ">{round(result_df['rate_filtered'][alias],1)}/5</p>
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

    col= st.columns((2,1,2))
    for i in range(nb):
        col[1].markdown(
            f"""<progress id="file" max="0.5" value="{result_df['metric sim_ratio'][i]}" style="margin-right:0px"></progress><br/><br/><br/>""",
            unsafe_allow_html=True)
        with col[0]:
            st.markdown(f"<h3>{result_df['name'][i]}</h3><br/>", unsafe_allow_html=True)


    with col[2]:
        folium_static(m, width=700, height=400)
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown(f"""<h3 style="text-align:center;
                        font-family:Baskerville, Baskerville Old Face, Garamond, Times New Roman, sans-serif">
                        Why you have to go !!!</h3><br/> """, unsafe_allow_html=True)

    st.markdown("""
                    "<span style='background-color:rgba(200,147.70981073379517,0,1)'>i forgot this place was vegan until i got there </span><span style='background-color:rgba(200,203.74802505970001,0,1)'> that's what happens when you have a running list of restaurants to visit in paris </span><span style='background-color:rgba(200,255,0,1)'> but seriously, this place is sooo good </span><span style='background-color:rgba(200,110.4891774058342,0,1)'> order l'allume, potatoes wedges and pay an extra euro for a beer </span>"<span style='background-color:rgba(200,109.5431873500347,0,1)'>i pretty much walked across paris to get to this spot and it was well worth the trek </span><span style='background-color:rgba(200,230.771965622901917,0,1)'> the place is quaint but cute </span><span style='background-color:rgba(200,245.490173161029816,0,1)'> i had the veggie burger with bar-b-que sauce on it, i don't quite remember it's name on the menu </span><span style='background-color:rgba(200,243.81418925523758,0,1)'> i ordered the meal the frites and a drink </span><span style='background-color:rgba(200,178.94982290267944,0,1)'> the burger was so fresh </span><span style='background-color:rgba(200,190.77875679731369,0,1)'> every bite was tasty and flavorful </span><span style='background-color:rgba(200,186.96417135000229,0,1)'> the frites where quite testy as well </span><span style='background-color:rgba(200,1614398378133774,0,1)'> i loved the upstairs sitting area </span><span style='background-color:rgba(200,255,0,1)'> it's cozy and comfy </span><span style='background-color:rgba(200,234.59012246131897,0,1)'> i was thankful for the wifi </span><span style='background-color:rgba(200,190.29720097780228,0,1)'> i'll definitely be back to hank on my next visit to paris veggie burgers in paris </span>"<br/>
                    "<span style='background-color:rgba(200,78.40744164586067,0,1)'>vegan burgers </span><span style='background-color:rgba(200,107.78531029820442,0,1)'> i've been strangely on a burger craving since in paris and spotted this on yelp with great reviews </span><span style='background-color:rgba(200,186.7808541059494,0,1)'> did not disappoint </span><span style='background-color:rgba(200,145.00488758087158,0,1)'> friendly service with english menu </span><span style='background-color:rgba(200,144.35372400283813,0,1)'> both hubs and i ordered the le grand menu with burger friesdessertdrink for euros </span><span style='background-color:rgba(200,140.71467417478561,0,1)'> deal </span><span style='background-color:rgba(200,42.6874584108591,0,1)'> i had the fig sauce, hubs had the tomatoe sauce, we both loved our burgers </span><span style='background-color:rgba(200,152.06384563446045,0,1)'> moist, flavorful and filling </span><span style='background-color:rgba(200,128.28458195924759,0,1)'> like everyone else said, potatoe wedges were awesome </span><span style='background-color:rgba(200,146.35313135385513,0,1)'> i loved my carrot cake and hubs enjoyed his choc chip cookie </span><span style='background-color:rgba(200,144.0462749004364,0,1)'> cute quaint upstairs and food was ready quickly </span><span style='background-color:rgba(200,255,0,1)'> getting quite the vegan burger fix in paris, i'm sure i'm going to go through withdrawals </span><span style='background-color:rgba(200,167.557668030262,0,1)'> le grand menu </span><span style='background-color:rgba(200,95.993834733963,0,1)'> burger, potatoe wedges and carrot cake </span>"<br/>
                    "<span style='background-color:rgba(200,170.89054554700851,0,1)'>literally best burgers ever </span><span style='background-color:rgba(200,255,0,1)'> quick service but no fast food atmosphere </span><span style='background-color:rgba(200,210.34319490194321,0,1)'> on the side the fried potatoes were tasty, not to mention the vegannaise was a true cherry on top </span><br/>" """,
                unsafe_allow_html=True)
