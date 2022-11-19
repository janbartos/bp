import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy import stats

rc('mathtext', default='regular')



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

df_import = pd.read_csv("df_data_" + languages.get(country) + ".csv")
df_import = df_import.drop(['2021'], axis=1)
df_transposed = df_import.set_index("keyword").T

corr = st.slider('Select desired Pearson correlation', -1.0, 1.0, (-0.5, 0.5))

df_corr = pd.read_csv("df_data_" + languages.get(country) + "_corr.csv")


#df_corr['fertility'].between(corr[0], corr[1], inclusive=False).values
if len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]) != 0 :
    keyword = st.selectbox(
        'Select keyword ' + str(len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")])) + " available" ,
    #df_import["keyword"].values
        df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]
    #df_corr['fertility'].between(corr[0], corr[1], inclusive=False).values
    )

df_fertility = pd.read_csv("fr.csv")
df_stats = pd.DataFrame()
df_stats["Data"] = df_transposed[keyword].values
df_stats["FTR"] = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values



col1, col2, col3, col4, col5 = st.columns(5)
pearson = stats.pearsonr(df_transposed[keyword].values,df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values)
col1.metric("Pearson correlation", round(pearson[0], 4))
col2.metric("p-Value", round(pearson[1], 5))
col3.metric("Covariance", round(df_stats.cov()["Data"].values[1],4))
spearman = stats.spearmanr(df_transposed[keyword].values,df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values)
col4.metric("Spearman correlation", round(spearman[0], 4))
col5.metric("p-Value", round(spearman[1], 5))




if len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]) != 0 :
    time = np.arange(2004, 2021)
    ftr = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values
    key_data = df_transposed[keyword].values





    #





    #

    fig = plt.figure()
    ax = fig.add_subplot(111)

    lns1 = ax.plot(time, ftr, '-', label='FTR in ' + country)
    ax2 = ax.twinx()
    lns2 = ax2.plot(time, key_data, '-r', label=keyword)

    # added these three lines
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.grid()
    ax.set_xlabel("Years")
    ax.set_ylabel(r"Fertility")
    ax2.set_ylabel(r"Searched")
    st.pyplot(fig)


    slope, intercept, r_value, p_value, std__err = stats.linregress(ftr, key_data)
    col6, col7, col8, col9, col10 = st.columns(5)

    col6.metric("Slope", round(slope, 4))
    col7.metric("Intercept", round(intercept, 5))
    col8.metric("R - value", round(r_value, 4))

    col9.metric("p-Value", round(p_value, 4))
    col10.metric("std_err", round(std__err, 5))


    fig2, ax3 = plt.subplots()




    abline_values = [slope * i + intercept for i in ftr]


    ax3.plot(ftr, abline_values, 'b')
    ax3.plot(ftr, key_data, '--', label = 'original data')
    #ax3.plot(ftr, intercept + (slope * ftr), "r", label = "fitted line")

    st.pyplot(fig2)