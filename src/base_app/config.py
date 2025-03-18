import streamlit as st

def default(title = "Page title", icon="", layout="wide", sidebar="collapsed"):
    st.set_page_config(title, icon, layout, sidebar)
