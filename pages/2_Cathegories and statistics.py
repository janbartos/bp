import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy import stats


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "black",
    "axes.facecolor": "white",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})


st.title("FTR analysis using Google Trends and Google Ngram data")

google = st.selectbox(
    'Select source',
    ('Google Trends', 'Google Ngram')
)

languages = {
    "Czechia": "cz",
    "Brasil": "br",
    "USA": "us",
    "Spain": "es",
    "Netherlands": "nl",
    "Germany": "de",
    "France": "fr"
}

fertility_codes = {
    "br": 'BRA',
    "cz": 'CZE',
    "de": 'DEU',
    "es": 'ESP',
    "fr": 'FRA',
    "nl": 'NLD',
    "us": 'USA'
}

country = st.selectbox(
    'Select country',
    languages.keys())

df_import = pd.read_csv("save2/data_groupby_" + languages.get(country) + ".csv")


cathegory = st.selectbox(
        'Select cathegory ',
    #df_import["keyword"].values
        df_import["Cathegory"].unique()
    #df_corr['fertility'].between(corr[0], corr[1], inclusive=False).values
    )