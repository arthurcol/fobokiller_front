import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64

LOGO_IMAGE = "test.jpg"
#mapimage = ...
st.markdown("""
    <style>
    .container {
        display: flex;
        justify-content: space-evenly;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:30px !important;
        color: #f9a49b !important;
        padding: 35px !important;
    }
    .logo-img {
        float:right;
        height: 700px;
        width: 600px;
        object-fit: cover;
    }
    </style>
    """,
            unsafe_allow_html=True)
st.markdown(f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">Logo Much ?</p>
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
    </div>
    """,
            unsafe_allow_html=True)
