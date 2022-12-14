import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy import stats
from scipy.optimize import curve_fit
from math import exp


from decimal import Decimal





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


st.title("TFR analysis using Google Trends data")


languages = {
    "Czech Republic": "cz",
    "Brazil": "br",
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

df_import = pd.read_csv("data/data_groupby/df_data_groupby_" + languages.get(country) + ".csv")
df_import = df_import.drop(['2021'], axis=1)
df_transposed = df_import.set_index("Cathegory").T



category = st.selectbox(
        'Select category ',
        df_import["Cathegory"].unique()
    )

df_fertility = pd.read_csv("data/fr.csv")

df_stats = pd.DataFrame()
df_stats["Data"] = df_transposed[category].values
df_stats["TFR"] = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:17]

df_fert = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values[:17]

df_sample_size = pd.read_csv("data/df_data/df_data_" + languages.get(country) + ".csv")
st.subheader('Sample size: ' + str(len(df_sample_size[df_sample_size["Cathegory"] == category])))

col1, col2, col3, col4, col5 = st.columns(5)

pearson = stats.pearsonr(df_stats["Data"].values, df_stats["TFR"].values)
col1.metric("Pearson correlation", round(pearson[0], 4))
col2.metric("p-Value", '%.2E' % pearson[1])
col3.metric("Covariance", round(df_stats.cov()["Data"].values[1], 4))
spearman = stats.spearmanr(df_stats["Data"].values, df_stats["TFR"].values)
col4.metric("Spearman correlation", round(spearman[0], 4))
col5.metric("p-Value", '%.2E' % spearman[1])

time = np.arange(2004, 2021)
ftr = df_stats["TFR"].values
key_data = df_stats["Data"].values

fig = plt.figure()
ax = fig.add_subplot(111)

lns1 = ax.plot(time, ftr, '-', label='TFR in ' + country)
ax2 = ax.twinx()
lns2 = ax2.plot(time, key_data, '-r', label=category)


lns = lns1 + lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
ax.set_xlabel("Years")
ax.set_ylabel(r"Fertility")
ax2.set_ylabel(r"Data")
st.pyplot(fig)

st.header('Regression')

slope, intercept, r_value, p_value, std__err = stats.linregress(key_data, ftr)
col6, col7, col8, col9, col10 = st.columns(5)

col6.metric("Slope", round(slope, 4))
col7.metric("Intercept", round(intercept, 4))
col8.metric("R - value", round(r_value, 4))

col9.metric("p-Value", '%.2E' % p_value )
col10.metric("std_err", round(std__err, 4))

y = ftr
x = key_data

fig2, ax3 = plt.subplots()

polyline = np.linspace(min(x), max(x), 17)


model = np.poly1d(np.polyfit(x, y, 2))


abline_values = [slope * i + intercept for i in key_data]

ax3.plot(key_data, abline_values, 'b', label="linear regression")
ax3.plot(key_data, ftr, 'ro', label='original data')
ax3.plot(polyline, model(polyline), label="y=%sx^2 %s*x %s" % (fmt_float(model[2]), fmt_float1(model[1]), fmt_float1(model[0])))

ax3.legend(loc='best', fancybox=True, shadow=True)
ax3.grid()
ax3.set_xlabel(r"Data")
ax3.set_ylabel(r"Fertility rate")

st.pyplot(fig2)





