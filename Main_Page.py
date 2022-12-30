import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components

rc('mathtext', default='regular')



st.set_page_config(
    page_title="Index"
)

st.write("# Total fertility rate analysis with Google Trends and Google Ngram")

st.markdown("Please select a demo located in left menu")
st.sidebar.success("Select a demo above.")

