import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import mpld3




def subplots(nrows=1, ncols=1, **kwargs):
    fig, ax = plt.subplots(nrows, ncols, **kwargs)
    return fig, ax

def line_plot(ax, x, y, **kwargs):
    ax.plot(x, y, **kwargs)
    return ax

def show_plot(fig, **kwargs):
    if type(fig) == matplotlib.figure.Figure:
        return st.pyplot(fig, **kwargs)
    if type(fig) == str:
        return st.components.v1.html(fig, **kwargs)

def make_interactive(fig, **kwargs):
    fig_html = mpld3.fig_to_html(fig)
    return fig_html
