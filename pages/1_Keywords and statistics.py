import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy.optimize import curve_fit
from scipy import stats

rc('mathtext', default='regular')


def func1(x, a, b, c):
    return a*x**2+b*x+c

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
    "Czech republic": "cz",
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

corr = st.slider('Select desired Pearson correlation', -1.0, 1.0, (0.7, 1.0))


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
df_stats["FTR"] = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:17]

if len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]) != 0 :

    col1, col2, col3, col4, col5 = st.columns(5)
    pearson = stats.pearsonr(df_transposed[keyword].values,df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:17])
    col1.metric("Pearson correlation", round(pearson[0], 4))
    col2.metric("p-Value", round(pearson[1], 5))
    col3.metric("Covariance", round(df_stats.cov()["Data"].values[1],4))
    spearman = stats.spearmanr(df_transposed[keyword].values,df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:17])
    col4.metric("Spearman correlation", round(spearman[0], 4))
    col5.metric("p-Value", round(spearman[1], 5))




if len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]) != 0 :
    time = np.arange(2004, 2021)
    ftr = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:17]
    key_data = df_transposed[keyword].values


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
    ax.set_ylabel(r"Fertility rate")
    ax2.set_ylabel(r"Searched")
    st.pyplot(fig)

    st.header('Linear regression')

    slope, intercept, r_value, p_value, std__err = stats.linregress(key_data,ftr)
    col6, col7, col8, col9, col10 = st.columns(5)

    col6.metric("Slope", round(slope, 4))
    col7.metric("Intercept", round(intercept, 5))
    col8.metric("R - value", round(r_value, 4))

    col9.metric("p-Value", round(p_value, 4))
    col10.metric("std_err", round(std__err, 5))


    fig2, ax3 = plt.subplots()

    y = ftr
    x = key_data

    params, _ = curve_fit(func1, x, y)
    a, b, c = params[0], params[1], params[2]
    yfit1 = a * x ** 2 + b * x + c

    abline_values = [slope * i + intercept for i in key_data]



    ax3.plot(key_data, abline_values, 'b' , label = "linear regression")
    ax3.plot(key_data, ftr, 'ro', label = 'original data')
    ax3.plot(x, yfit1, label="y=%5.f*x^2+%5.f*x+%5.3f" % tuple(params))
    ax3.legend(["FTR in " + country, str(keyword)])
    ax3.legend(loc='best', fancybox=True, shadow=True)
    ax3.grid()
    ax3.set_xlabel(r"Searched")
    ax3.set_ylabel(r"Fertility rate")

    st.pyplot(fig2)

    ## sesion_state