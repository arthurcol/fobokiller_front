from geopy.geocoders import Nominatim
import streamlit as st
import geocoder
loc = Nominatim(user_agent="GetLoc")

getLoc = loc.geocode("21 rue fille du calvaire")

st.write(getLoc)
g = geocoder.ip('me')
st.write(g.latlng)
