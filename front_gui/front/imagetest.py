'ok pour image'

from PIL import Image
import streamlit as st

img = Image.open("test.jpg")

st.image(img, width=600)

img = Image.open("test2.jpg")

st.image(img, width=600)

#soit fonction ajout de fond blanc ????
#soit autre moyen pour redim ???
