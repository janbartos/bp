import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy.optimize import curve_fit
from scipy import stats

rc('mathtext', default='regular')



def fmt_float(q):
    s = '%.4g' % q
    if s.endswith('.0000'):
        s = s[:-5]
    return s

def fmt_float1(q):

    s = '%.4g' % q
    if s.endswith('.0000'):
        s = s[:-5]
    if q >= 0:
        s = "+" + s
    return s

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
    "Czech Republic": "cz",
    "Brazil": "br",
    "USA": "us",
    "Spain": "es",
    "Netherlands": "nl",
    "Germany": "de",
    "France": "fr"
}
languages_ngram = {
    "USA": "us",
    "Spain": "es",
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

langs = {
    "br" : "PT-BR",
    "us" : "EN",
    "cz" : "CS",
    "de" : "DE",
    "fr" : "FR",
    "nl" : "NL",
    "es" : "ES",
}

if google == "Google Trends":
    selected = languages
else:
    selected = languages_ngram

country = st.selectbox(
    'Select country',
    selected.keys())


if google == "Google Trends":
    df_import = pd.read_csv("data/df_data/df_data_" + languages.get(country) + ".csv")
    df_import = df_import.drop(['2021'], axis=1)

    df_import = df_import.drop(['Cathegory'], axis=1)
    df_corr = pd.read_csv("data//df_data_corr/df_data_" + languages.get(country) + "_corr.csv")
else:
    df_import = pd.read_csv("data/ngram/df_" + languages.get(country) + "_ngram.csv")
    df_corr = pd.read_csv("data/ngram/df_data_" + languages.get(country) + "_ngram_corr.csv")

df_transposed = df_import.set_index("keyword").T

df_category = pd.read_csv("data/keyword_translations.csv")

corr = st.slider('Select desired Pearson correlation', -1.0, 1.0, (0.85, 1.0))


keyword = ""
selectBool = False

if len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]) != 0:
    keyword = st.selectbox(
        'Select keyword ' + str(len(df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")])) + " available" ,
        df_corr[df_corr['fertility'].between(corr[0], corr[1], inclusive="neither")]
    )
    selectBool = True


if keyword != "":
    st.caption('Category: ' + df_category.loc[df_category[langs.get(languages.get(country))] == keyword].Cathegory.values[0])
    if country != "USA":
        st.caption(
            'Keyword in English: ' + df_category.loc[df_category[langs.get(languages.get(country))] == keyword].EN.values[
                0])

    lenArr = 0

    df_fertility = pd.read_csv("data/fr.csv")
    df_stats = pd.DataFrame()


    if google == "Google Trends":
        lenArr = 17
    else:
        lenArr = 16
    df_stats["Data"] = df_transposed[keyword].values[:lenArr]
    df_stats["FTR"] = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:lenArr]



    col1, col2, col3, col4, col5 = st.columns(5)
    pearson = stats.pearsonr(df_stats["Data"].values, df_stats["FTR"].values)
    col1.metric("Pearson correlation", round(pearson[0], 4))
    col2.metric("p-Value", '%.2E' % pearson[1])
    col3.metric("Covariance", round(df_stats.cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_stats["Data"].values, df_stats["FTR"].values)
    col4.metric("Spearman correlation", round(spearman[0], 4))
    col5.metric("p-Value", '%.2E' % spearman[1])



    time = np.arange(2004, 2004 + lenArr)
    ftr = df_stats["FTR"].values
    key_data = df_stats["Data"].values

    fig = plt.figure()
    ax = fig.add_subplot(111)

    lns1 = ax.plot(time, ftr, '-', label='FTR in ' + country)
    ax2 = ax.twinx()
    lns2 = ax2.plot(time, key_data, '-r', label=keyword)


    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.grid()
    ax.set_xlabel("Years")
    ax.set_ylabel(r"Fertility rate")
    ax2.set_ylabel(r"Data")
    st.pyplot(fig)

    st.header('Regression')

    slope, intercept, r_value, p_value, std__err = stats.linregress(key_data,ftr)
    col6, col7, col8, col9, col10 = st.columns(5)

    col6.metric("Slope", round(slope, 4))
    col7.metric("Intercept", round(intercept, 5))
    col8.metric("R - value", round(r_value, 4))

    col9.metric("p-Value", '%.2E' % p_value)
    col10.metric("std_err", round(std__err, 5))


    fig2, ax3 = plt.subplots()

    y = ftr
    x = key_data



    polyline = np.linspace(min(x), max(x), lenArr)

    model = np.poly1d(np.polyfit(x, y, 2))


    abline_values = [slope * i + intercept for i in key_data]



    ax3.plot(key_data, abline_values, 'b' , label = "linear regression")
    ax3.plot(key_data, ftr, 'ro', label = 'original data')
    ax3.plot(polyline, model(polyline),
             label="y=%sx^2 %s*x %s" % (fmt_float(model[2]), fmt_float1(model[1]), fmt_float1(model[0])))
    ax3.legend(["FTR in " + country, str(keyword)])
    ax3.legend(loc='best', fancybox=True, shadow=True)
    ax3.grid()
    ax3.set_xlabel(r"Data")
    ax3.set_ylabel(r"Fertility rate")

    st.pyplot(fig2)

