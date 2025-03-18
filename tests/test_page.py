import sys, os
path = os.getcwd()+"\\src\\"
if path not in sys.path:
    sys.path.insert(0, path)

import base_app

base_app.config.default("Test")


header_elements = [
{
    "page_name": "Home",
    "filepath": "./pages/home.py" ,
    "icon": "🏠"
},
{
    "page_name": "Tables",
    "filepath": "./pages/tables.py" ,
    "icon": "🗃️"
},

]

import streamlit as st

st.cache_data

base_app.headers.header(header_elements)