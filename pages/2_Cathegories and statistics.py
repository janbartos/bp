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

df_import = pd.read_csv("save2/df_data_groupby_" + languages.get(country) + ".csv")
df_import = df_import.drop(['2021'], axis=1)
df_transposed = df_import.set_index("Cathegory").T



cathegory = st.selectbox(
        'Select cathegory ',
    #df_import["keyword"].values
        df_import["Cathegory"].unique()
    #df_corr['fertility'].between(corr[0], corr[1], inclusive=False).values
    )

df_fertility = pd.read_csv("fr.csv")
df_stats = pd.DataFrame()
df_stats["Data"] = df_transposed[cathegory].values
df_stats["FTR"] = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values

df_sample_size = pd.read_csv("save2/df_data_" + languages.get(country) + " .csv")
st.subheader('Sample size: ' + str(len(df_sample_size["Cathegory" == cathegory].values)))

col1, col2, col3, col4, col5 = st.columns(5)
pearson = stats.pearsonr(df_transposed[cathegory].values,df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values)
col1.metric("Pearson correlation", round(pearson[0], 4))
col2.metric("p-Value", round(pearson[1], 5))
col3.metric("Covariance", round(df_stats.cov()["Data"].values[1],4))
spearman = stats.spearmanr(df_transposed[cathegory].values,df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values)
col4.metric("Spearman correlation", round(spearman[0], 4))
col5.metric("p-Value", round(spearman[1], 5))

time = np.arange(2004, 2021)
ftr = df_fertility[df_fertility.LOCATION == fertility_codes.get(languages.get(country))]['Value'].values
key_data = df_transposed[cathegory].values

fig = plt.figure()
ax = fig.add_subplot(111)

lns1 = ax.plot(time, ftr, '-', label='FTR in ' + country)
ax2 = ax.twinx()
lns2 = ax2.plot(time, key_data, '-r', label=cathegory)

# added these three lines
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
ax.set_xlabel("Years")
ax.set_ylabel(r"Fertility")
ax2.set_ylabel(r"Searched")
st.pyplot(fig)