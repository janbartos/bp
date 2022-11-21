import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy import stats
from scipy.optimize import curve_fit
from math import exp


st.title("Interesting outliers")

st.header('Fall of the left movement in Brasil')


df_fertility = pd.read_csv("fr.csv")

df_import = pd.read_csv("df_data_br.csv")
df_import = df_import.drop(['2021'], axis=1)
df_transposed = df_import.set_index("keyword").T


df_fert = df_fertility[df_fertility.LOCATION == "BRA"]['Value'].values[:17]

df_stats = pd.DataFrame()
df_stats["Data"] = df_transposed["guevara"].values
df_stats["FTR"] = df_fert

st.subheader('Guevara')
keyword = "guevara"

col1, col2, col3, col4, col5 = st.columns(5)
pearson = stats.pearsonr(df_transposed[keyword].values, df_fert)
col1.metric("Pearson correlation", round(pearson[0], 4))
col2.metric("p-Value", round(pearson[1], 5))
col3.metric("Covariance", round(df_stats.cov()["Data"].values[1],4))
spearman = stats.spearmanr(df_transposed[keyword].values, df_fert)
col4.metric("Spearman correlation", round(spearman[0], 4))
col5.metric("p-Value", round(spearman[1], 5))

st.subheader('Marx')

keyword = "marx"

df_stats = pd.DataFrame()
df_stats["Data"] = df_transposed[keyword].values

col6, col7, col8, col9, col10 = st.columns(5)
pearson = stats.pearsonr(df_transposed[keyword].values, df_fert)
col6.metric("Pearson correlation", round(pearson[0], 4))
col7.metric("p-Value", round(pearson[1], 5))
col8.metric("Covariance", round(df_stats.cov()["Data"].values[1],4))
spearman = stats.spearmanr(df_transposed[keyword].values, df_fert)
col9.metric("Spearman correlation", round(spearman[0], 4))
col10.metric("p-Value", round(spearman[1], 5))

st.subheader("Sindicatos - Work unions")

keyword = "sindicatos"

col11, col12, col13, col14, col15 = st.columns(5)
pearson = stats.pearsonr(df_transposed[keyword].values, df_fert)
col11.metric("Pearson correlation", round(pearson[0], 4))
col12.metric("p-Value", round(pearson[1], 5))
col13.metric("Covariance", round(df_stats.cov()["Data"].values[1],4))
spearman = stats.spearmanr(df_transposed[keyword].values, df_fert)
col14.metric("Spearman correlation", round(spearman[0], 4))
col15.metric("p-Value", round(spearman[1], 5))



time = np.arange(2004, 2021)
ftr = df_fertility[df_fertility.LOCATION == "BRA"]['Value'].values
Guevara_data = df_transposed["guevara"].values
Marx_data = df_transposed["marx"].values
Sindicatos_data = df_transposed["sindicatos"].values





fig = plt.figure()
ax = fig.add_subplot(111)

lns1 = ax.plot(time, ftr, '-', label='FTR in Brasil')
ax2 = ax.twinx()
lns2 = ax2.plot(time, Guevara_data, '-r', label="Guevara")
lns3 = ax2.plot(time, Marx_data, "-r", label="Marx")
lns4 = ax2.plot(time, Sindicatos_data, "-r", label="Sindicados")

# added these three lines
lns = lns1 + lns2 + lns4 + lns3
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
ax.set_xlabel("Years")
ax.set_ylabel(r"Fertility")
ax2.set_ylabel(r"Searched")
st.pyplot(fig)