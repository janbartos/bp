import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy import stats
from scipy.optimize import curve_fit
from math import exp
import altair as alt


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
df_stats["Data"] = df_transposed[keyword].values

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
lns3 = ax2.plot(time, Marx_data, "-o", label="Marx")
lns4 = ax2.plot(time, Sindicatos_data, "-b", label="Sindicados")

# added these three lines
lns = lns1 + lns2 + lns4 + lns3
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
ax.set_xlabel("Years")
ax.set_ylabel(r"Fertility")
ax2.set_ylabel(r"Searched")
st.pyplot(fig)

chart_data = pd.DataFrame({

     "Candidates": ["Luiz Inácio Lula da Silva", "José Serra", "Luiz Inácio Lula da Silva", "Geraldo Alckmin", "Dilma Rousseff", "José Serra", "Dilma Rousseff", "Aécio Neves",	"Fernando Haddad", "Jair Bolsonaro"],
     "Results":  [61.27, 38.73, 60.83, 39.17, 56.05, 43.95, 51.64, 48.36, 44.87, 55.13],
     "Year": [2002, 2002, 2006, 2006, 2010, 2010, 2014, 2014, 2018, 2018],
     "Party": ["PT", "PSDB", "PT", "PSDB", "PT", "PSDB", "PT", "PSDB", "PT", "PSL"]

})
#https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/unpd_egm_200203_countrypapers_what_will_happen_to_brazilian_fertility_goldani.pdf
bar_chart = alt.Chart(chart_data).mark_bar().encode(
        x="Year:O",
        y="Results:Q",
        color="Party:N",
        tooltip=['Candidates', 'Party', 'Results']
    )
st.altair_chart(bar_chart, use_container_width=True)

st.header('Universities in Americas')


df_import_br = pd.read_csv("save2/df_data_groupby_br.csv")
df_import_us = pd.read_csv("save2/df_data_groupby_us.csv")

df_fertility = pd.read_csv("fr.csv")

df_import_br = df_import_br.drop(['2021'], axis=1)
df_import_us = df_import_us.drop(['2021'], axis=1)

df_import_br = df_import_br.set_index("Cathegory").T
df_import_us = df_import_us.set_index("Cathegory").T

df_fert_us = df_fertility[df_fertility.LOCATION == "USA"]['Value'].values[:17]
df_fert_br = df_fertility[df_fertility.LOCATION == "BRA"]['Value'].values[:17]

time = np.arange(2004, 2021)

df_uni_us = pd.DataFrame()
df_uni_us["University"] = df_import_us["University"].values
df_uni_us["FTR"] = df_fert_us
df_uni_us["Time"] = time


df_uni_br = pd.DataFrame()
df_uni_br["University"] = df_import_br["University"].values
df_uni_br["FTR"] = df_fert_br
df_uni_br["Time"] = time


base1 = alt.Chart(df_uni_us).encode(alt.X('Time'))


a = base1.mark_line().encode(
    alt.Y('FTR', scale=alt.Scale(domain=(1.6, 2.15))), color='red'
)
b = base1.mark_line().encode(
    alt.Y('University', scale=alt.Scale(domain=(10, 45)))
)
c = alt.layer(a, b).resolve_scale(y='independent').interactive()

base2 = alt.Chart(df_uni_br).encode(alt.X('Time'))


d = base1.mark_line().encode(
    alt.Y('FTR', scale=alt.Scale(domain=(1.6, 2.15)))
)
e = base1.mark_line().encode(
    alt.Y('University', scale=alt.Scale(domain=(10, 45)))
)

f = alt.layer(a, b).resolve_scale(y='independent').interactive()



#chart2 = alt.Chart(df_uni_br).mark_line()

st.altair_chart(c)
st.altair_chart(f)

