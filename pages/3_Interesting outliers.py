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

def func1(x, a, b, c):
    return a*x**2+b*x+c

st.title("Interesting outliers")


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Fall of the left in Brasil", "Universities in Americas", "Consumerism in USA", "Education in Czechia" ,"Sleep deprivation"])


with tab1:

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

with tab2:

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



    st.subheader('University category in USA')


    col16, col17, col18, col19, col20 = st.columns(5)
    pearson = stats.pearsonr(df_uni_us["University"].values , df_uni_us["FTR"].values )
    col16.metric("Pearson correlation", round(pearson[0], 4))
    col17.metric("p-Value", round(pearson[1], 5))
    col18.metric("Covariance", round(df_uni_us[["University", "FTR"]].cov()["University"].values[1],4))
    spearman = stats.spearmanr(df_uni_us["University"].values, df_uni_us["FTR"].values)
    col19.metric("Spearman correlation", round(spearman[0], 4))
    col20.metric("p-Value", round(spearman[1], 5))

    st.subheader('University category in Brazil')


    col21, col22, col23, col24, col25 = st.columns(5)
    pearson = stats.pearsonr(df_uni_br["University"].values , df_uni_br["FTR"].values )
    col21.metric("Pearson correlation", round(pearson[0], 4))
    col22.metric("p-Value", round(pearson[1], 5))
    col23.metric("Covariance", round(df_uni_br[["University", "FTR"]].cov()["University"].values[1],4))
    spearman = stats.spearmanr(df_uni_br["University"].values, df_uni_br["FTR"].values)
    col24.metric("Spearman correlation", round(spearman[0], 4))
    col25.metric("p-Value", round(spearman[1], 5))




    base1 = alt.Chart(df_uni_us, title="🔵 University  🔴 FTR in USA" ).encode(alt.X('Time'))

    a = base1.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.6, 2.15)))
    )
    b = base1.mark_line().encode(
        alt.Y('University', scale=alt.Scale(domain=(10, 45)))
    )
    c = alt.layer(a, b).resolve_scale(y='independent').interactive()

    base2 = alt.Chart(df_uni_br, title= "🔵 University  🔴 FTR in Brazil").encode(alt.X('Time'))


    d = base2.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.7, 2.05)))
    )
    e = base2.mark_line().encode(
        alt.Y('University', scale=alt.Scale(domain=(4, 18)))
    )

    f = alt.layer(d, e).resolve_scale(y='independent').interactive()

    st.altair_chart(c | f, use_container_width=True)

    school_usa_enrollment = pd.DataFrame({

         "Enrollment": [17272044, 17487475, 17754230, 18258138, 19081686, 20313594, 21019438, 21010590,	20644478, 20376677, 20209092, 19988204, 19846904, 19778151, 19651412, 19630178, 18991798],
         "Time":       [2004,     2005,     2006,     2007,     2008,     2009,     2010,     2011,     2012,     2013,     2014,     2015,     2016,     2017,     2018,     2019,     2020]
    })

    bar_chart = alt.Chart(school_usa_enrollment).mark_bar().encode(
            x="Time:O",
            y="Enrollment:Q",
            tooltip=['Enrollment', 'Time']
        )
    st.subheader('University enrollment in USA')
    st.altair_chart(bar_chart, use_container_width=True)

#https://educationdata.org/college-enrollment-statistics
with tab3:
    st.header('Consumerism in USA')

    df_import_us = pd.read_csv("save2/df_data_groupby_us.csv")

    df_fertility = pd.read_csv("fr.csv")

    df_import_us = df_import_us.drop(['2021'], axis=1)

    df_import_us = df_import_us.set_index("Cathegory").T

    df_fert_us = df_fertility[df_fertility.LOCATION == "USA"]['Value'].values[:17]

    time = np.arange(2004, 2021)

    df_con_us = pd.DataFrame()
    df_con_us["Consumerism"] = df_import_us["Consumerism"].values
    df_con_us["FTR"] = df_fert_us
    df_con_us["Time"] = time


    st.subheader('Consumerism category in USA')


    col1, col2, col3, col4, col5 = st.columns(5)
    pearson = stats.pearsonr(df_con_us["Consumerism"].values , df_con_us["FTR"].values )
    col1.metric("Pearson correlation", round(pearson[0], 4))
    col2.metric("p-Value", round(pearson[1], 5))
    col3.metric("Covariance", round(df_con_us[["Consumerism", "FTR"]].cov()["Consumerism"].values[1],4))
    spearman = stats.spearmanr(df_con_us["Consumerism"].values, df_con_us["FTR"].values)
    col4.metric("Spearman correlation", round(spearman[0], 4))
    col5.metric("p-Value", round(spearman[1], 5))


    base1 = alt.Chart(df_con_us, title="🔵 Consumerism  🔴 FTR in USA" ).encode(alt.X('Time'))

    a = base1.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.6, 2.15)))
    )
    b = base1.mark_line().encode(
        alt.Y('Consumerism', scale=alt.Scale(domain=(10, 45)))
    )
    c = alt.layer(a, b).resolve_scale(y='independent').interactive()

    st.altair_chart(c)
    #https://www.pnas.org/doi/10.1073/pnas.1909857117

with tab4:
    st.header('Education in Czechia')
    df_import_cz = pd.read_csv("save2/df_data_groupby_cz.csv")

    df_fertility = pd.read_csv("fr.csv")

    df_import_cz = df_import_cz.drop(['2021'], axis=1)

    df_import_cz = df_import_cz.set_index("Cathegory").T

    df_fert_cz = df_fertility[df_fertility.LOCATION == "CZE"]['Value'].values[:17]

    time = np.arange(2004, 2021)

    df_edu_cz = pd.DataFrame()
    df_edu_cz["Education"] = df_import_cz["Education"].values
    df_edu_cz["FTR"] = df_fert_cz
    df_edu_cz["Time"] = time


    st.subheader('Education category in Czechia')


    col1, col2, col3, col4, col5 = st.columns(5)
    pearson = stats.pearsonr(df_edu_cz["Education"].values , df_edu_cz["FTR"].values )
    col1.metric("Pearson correlation", round(pearson[0], 4))
    col2.metric("p-Value", round(pearson[1], 5))
    col3.metric("Covariance", round(df_edu_cz[["Education", "FTR"]].cov()["Education"].values[1],4))
    spearman = stats.spearmanr(df_edu_cz["Education"].values, df_edu_cz["FTR"].values)
    col4.metric("Spearman correlation", round(spearman[0], 4))
    col5.metric("p-Value", round(spearman[1], 5))


    base1 = alt.Chart(df_edu_cz, title="🔵 Education  🔴 FTR in Czechia" ).encode(alt.X('Time'))

    a = base1.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.2, 1.75)))
    )
    b = base1.mark_line().encode(
        alt.Y('Education', scale=alt.Scale(domain=(26, 40)))
    )
    c = alt.layer(a, b).resolve_scale(y='independent').interactive()

    st.altair_chart(c)

    df_import = pd.read_csv("df_data_cz.csv")
    df_import = df_import.drop(['2021'], axis=1)
    df_transposed = df_import.set_index("keyword").T




    df_stats = pd.DataFrame()
    df_stats["Data"] = df_transposed["guevara"].values
    df_stats["FTR"] = df_fert_cz

    st.subheader('Univerzita')
    keyword = "Univerzita"

    col1, col2, col3, col4, col5 = st.columns(5)
    pearson = stats.pearsonr(df_transposed[keyword].values, df_fert_cz)
    col1.metric("Pearson correlation", round(pearson[0], 4))
    col2.metric("p-Value", round(pearson[1], 5))
    col3.metric("Covariance", round(df_stats.cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_transposed[keyword].values, df_fert_cz)
    col4.metric("Spearman correlation", round(spearman[0], 4))
    col5.metric("p-Value", round(spearman[1], 5))

    st.subheader('Zeměpis')

    keyword = "zeměpis"

    df_stats["Data"] = df_transposed[keyword].values

    col6, col7, col8, col9, col10 = st.columns(5)
    pearson = stats.pearsonr(df_transposed[keyword].values, df_fert_cz)
    col6.metric("Pearson correlation", round(pearson[0], 4))
    col7.metric("p-Value", round(pearson[1], 5))
    col8.metric("Covariance", round(df_stats.cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_transposed[keyword].values, df_fert_cz)
    col9.metric("Spearman correlation", round(spearman[0], 4))
    col10.metric("p-Value", round(spearman[1], 5))

    st.subheader("Chemie")

    keyword = "chemie"
    df_stats["Data"] = df_transposed[keyword].values

    col11, col12, col13, col14, col15 = st.columns(5)
    pearson = stats.pearsonr(df_transposed[keyword].values, df_fert_cz)
    col11.metric("Pearson correlation", round(pearson[0], 4))
    col12.metric("p-Value", round(pearson[1], 5))
    col13.metric("Covariance", round(df_stats.cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_transposed[keyword].values, df_fert_cz)
    col14.metric("Spearman correlation", round(spearman[0], 4))
    col15.metric("p-Value", round(spearman[1], 5))

    st.subheader("Vysoká škola")

    keyword = "vysoká škola"
    df_stats["Data"] = df_transposed[keyword].values

    col16, col17, col18, col19, col20 = st.columns(5)
    pearson = stats.pearsonr(df_transposed[keyword].values, df_fert_cz)
    col16.metric("Pearson correlation", round(pearson[0], 4))
    col17.metric("p-Value", round(pearson[1], 5))
    col18.metric("Covariance", round(df_stats.cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_transposed[keyword].values, df_fert_cz)
    col19.metric("Spearman correlation", round(spearman[0], 4))
    col20.metric("p-Value", round(spearman[1], 5))

    ftr = df_fert
    y1 = df_transposed["vysoká škola"].values
    y2 = df_transposed["chemie"].values
    y3 = df_transposed["zeměpis"].values
    y4 = df_transposed["Univerzita"].values



#Education
#univerzita, zeměpis, chemie, vysoká škola
with tab5:
    st.header("How to sleep in USA")


    df_fertility = pd.read_csv("fr.csv")

    df_import_br = pd.read_csv("df_data_br.csv")
    df_import_nl = pd.read_csv("df_data_nl.csv")
    df_import_us = pd.read_csv("df_data_us.csv")


    df_import_br = df_import_br.drop(['2021'], axis=1)
    df_import_nl = df_import_nl.drop(['2021'], axis=1)
    df_import_us = df_import_us.drop(['2021'], axis=1)

    df_import_br = df_import_br.set_index("keyword").T
    df_import_nl = df_import_nl.set_index("keyword").T
    df_import_us = df_import_us.set_index("keyword").T


    df_fert_br = df_fertility[df_fertility.LOCATION == "BRA"]['Value'].values[:17]
    df_fert_nl = df_fertility[df_fertility.LOCATION == "NLD"]['Value'].values[:17]
    df_fert_us = df_fertility[df_fertility.LOCATION == "USA"]['Value'].values[:17]

    keyword_br = "como dormir"

    df_stats_br = pd.DataFrame()
    df_stats_br["Data"] = df_import_br[keyword_br].values
    df_stats_br["FTR"] = df_fert_br
    df_stats_br["Time"] = range(2004, 2021)

    st.subheader(keyword_br)
    keyword = keyword_br

    col1, col2, col3, col4, col5 = st.columns(5)
    pearson = stats.pearsonr(df_import_br[keyword].values, df_fert_br)
    col1.metric("Pearson correlation", round(pearson[0], 4))
    col2.metric("p-Value", round(pearson[1], 5))
    col3.metric("Covariance", round(df_stats_br[["Data", "FTR"]].cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_import_br[keyword].values, df_fert_br)
    col4.metric("Spearman correlation", round(spearman[0], 4))
    col5.metric("p-Value", round(spearman[1], 5))



    keyword_nl = "slaaptekort"

    df_stats_nl = pd.DataFrame()
    df_stats_nl["Data"] = df_import_nl[keyword_nl].values
    df_stats_nl["FTR"] = df_fert_nl
    df_stats_nl["Time"] = range(2004, 2021)

    st.dataframe(df_stats_nl)

    st.subheader(keyword_nl)

    keyword = keyword_nl

    col6, col7, col8, col9, col10 = st.columns(5)
    pearson = stats.pearsonr(df_import_nl[keyword_nl].values, df_fert_nl)
    col6.metric("Pearson correlation", round(pearson[0], 4))
    col7.metric("p-Value", round(pearson[1], 5))
    col8.metric("Covariance", round(df_stats_nl[["Data", "FTR"]].cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_import_nl[keyword_nl].values, df_fert_nl)
    col9.metric("Spearman correlation", round(spearman[0], 4))
    col10.metric("p-Value", round(spearman[1], 5))

    keyword_us = "how to sleep"

    df_stats_us = pd.DataFrame()
    df_stats_us["Data"] = df_import_us[keyword_us].values
    df_stats_us["FTR"] = df_fert_us
    df_stats_us["Time"] = range(2004, 2021)

    st.subheader(keyword_us)

    keyword = keyword_us


    col11, col12, col13, col14, col15 = st.columns(5)
    pearson = stats.pearsonr(df_import_us[keyword].values, df_fert_us)
    col11.metric("Pearson correlation", round(pearson[0], 4))
    col12.metric("p-Value", round(pearson[1], 5))
    col13.metric("Covariance", round(df_stats_us[["Data", "FTR"]].cov()["Data"].values[1], 4))
    spearman = stats.spearmanr(df_import_us[keyword].values, df_fert_us)
    col14.metric("Spearman correlation", round(spearman[0], 4))
    col15.metric("p-Value", round(spearman[1], 5))

    base1 = alt.Chart(df_stats_us, title="🔵 University  🔴 FTR in USA" ).encode(alt.X('Time'))

    a = base1.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.6, 2.15)))
    )
    b = base1.mark_line().encode(
        alt.Y('Data', scale=alt.Scale(domain=(10, 45)))
    )
    c = alt.layer(a, b).resolve_scale(y='independent').interactive()

    base2 = alt.Chart(df_stats_br, title= "🔵 University  🔴 FTR in Brazil").encode(alt.X('Time'))


    d = base2.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.7, 2.05)))
    )
    e = base2.mark_line().encode(
        alt.Y('Data', scale=alt.Scale(domain=(4, 18)))
    )

    f = alt.layer(d, e).resolve_scale(y='independent').interactive()

    base3 = alt.Chart(df_stats_nl, title="🔵 University  🔴 FTR in USA").encode(alt.X('Time'))

    g = base3.mark_line(color='red').encode(
        alt.Y('FTR', scale=alt.Scale(domain=(1.7, 2.05)))
    )
    i = base3.mark_line().encode(
        alt.Y('Data', scale=alt.Scale(domain=(4, 18)))
    )

    j = alt.layer(g, i).resolve_scale(y='independent').interactive()

    st.altair_chart(c | f | j, use_container_width=True)

#slaap netherlands
#como dorme brasil