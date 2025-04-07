from base_app import plots
import streamlit as st
import numpy as np

x = np.arange(0,100,1)
y = np.random.rand(100)

fig, ax = plots.subplots(figsize=(10,4))
ax = plots.line_plot(ax, x, y)
fig = plots.make_interactive(fig,  height=1000)
plots.show_plot(fig)
st.write(fig)