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

st.subheader('Guevara')
st.subheader('Marx')
st.subheader("Sindicatos - Work unions")

df_fertility = pd.read_csv("fr.csv")

df_import = pd.read_csv("df_data_br.csv")
df_import = df_import.drop(['2021'], axis=1)
df_transposed = df_import.set_index("keyword").T

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