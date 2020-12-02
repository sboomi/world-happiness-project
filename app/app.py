import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pymysql
import seaborn as sns
import numpy as np
import plotly.graph_objs as go

@st.cache(suppress_st_warning=True)
def generate_data():
    frames = {}

    MYSQL_DATABASE='WH_docker'
    MYSQL_USER= 'sboomi'
    MYSQL_PASSWORD= 'sboomi'
    MYSQL_ROOT_PASSWORD= 'root2020'
    host="127.0.0.1:3306" #'0.0.0.0:3306'
    DATABASE_URL= "mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=MYSQL_USER,host=host,pw=MYSQL_PASSWORD,db=MYSQL_DATABASE)
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    reqprox= connection.execute('SHOW TABLES')
    
    for i, row in enumerate(reqprox):
        table, = row
        frames[table] = pd.read_sql_table(table, connection).drop('index', axis=1)  
    connection.close()
    return frames

frames = generate_data()

topic_box = st.sidebar.selectbox(
    "What would you like to see?",
    ("Happiness indicators", "Suicide indicators", "Homicide indicators")
)

st.title('World Happiness App')

st.markdown('World Happiness app lets you explore the state of the world!')

if topic_box=="Happiness indicators":
    df = frames['happy']
    st.header('Happiness indicators')

    # Insert avg map here
    avg_score_series = df.groupby('country').mean()['score']
    data = { 'type':'choropleth',
       'locations': avg_score_series.index,
       'locationmode': 'country names',
       'colorscale': 'viridis',
       'z':avg_score_series.values}
    avg_h_map = go.Figure(data=[data])
    st.plotly_chart(avg_h_map)

    # Insert scroller
    list_countries = tuple(np.sort(df.country.unique()).tolist())
    country = st.selectbox(
        "Select a country",
        list_countries)

    stats_country = df[df.country==country]

    col_stats, col_other = st.beta_columns(2)
    
    col_stats.subheader("Happiness score evolution per year")
    
    fig, ax = plt.subplots()
    g = sns.lineplot(data=stats_country, x="year", y="score", ax=ax)
    col_stats.pyplot(fig)
    
    col_other.subheader("Average indicators")
    mean_stats = stats_country.describe().loc['mean']
    col_other.dataframe(stats_country.describe().loc['mean',
    ['freedom', 'economy', 'health', 'corruption', 'social_support', 'generosity']])
    


elif topic_box=="Homicide indicators":
    df = frames['danger_100k']
    st.header('Homicide indicators')

    col_numbers, col_map = st.beta_columns([1,3])

    list_countries = tuple(np.sort(df.country.unique()).tolist())
    col_numbers.subheader("Number of homicides per year")
    country = col_numbers.selectbox(
        "Select a country",
        list_countries)

    stats_country = df[df.country==country]

    if stats_country.shape[0]==1:
        col_numbers.text(f"Year: {stats_country['year'].values[0]}")
        col_numbers.write(f"Number of murders: {stats_country['count'].values[0]}")
    else:
        fig, ax = plt.subplots()
        g = sns.lineplot(data=stats_country, x="year", y="count", ax=ax)
        col_numbers.pyplot(fig)

    col_map.subheader("Average rate of homicides")
    plotly_data = { 'type':'choropleth',
       'locations': df.country,
       'locationmode': 'country names',
       'colorscale': 'viridis',
       'reversescale': True,
       'z':df.groupby('country').mean().rate}
    col_map.plotly_chart(go.Figure(data=[plotly_data]))


elif topic_box=='Suicide indicators':
    df = frames['suicide_100k'].copy()
    df = df.dropna(axis=0)
    df.sex = df.sex.apply(lambda x: x.lower().strip())
    st.header('Suicide indicators')

    # Insert avg map here
    avg_score_series = df[df.sex=="both sexes"].groupby('country').mean()['suicide_rate']
    plotly_data = { 'type':'choropleth',
       'locations': avg_score_series.index,
       'locationmode': 'country names',
       'colorscale': 'viridis',
       "reversescale": True,
       'z':avg_score_series.values}
    avg_s_map = go.Figure(data=[plotly_data])
    st.plotly_chart(avg_s_map)

    # Insert scroller
    list_countries = tuple(np.sort(df.country.unique()).tolist())
    country = st.selectbox(
        "Select a country",
        list_countries)

    stats_country = df[df.country==country]

    col_1, col_2 = st.beta_columns(2)
    col_1.subheader("Evolution of suicide rate per sex")

    fig, ax = plt.subplots()
    g = sns.lineplot(data=stats_country[stats_country['sex']!="both sexes"], x="year", y="suicide_rate", hue="sex", ax=ax)
    col_1.pyplot(fig)

    col_2.subheader("Whatever")
