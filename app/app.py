import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql
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
elif topic_box=="Homicide indicators":
    df = frames['danger_100k']
    st.header('Homicide indicators')

    col_numbers, col_map = st.beta_columns(2)

    list_countries = tuple(np.sort(df.country.unique()).tolist())
    col_numbers.subheader("Number of homicides per year")
    country = col_numbers.selectbox(
        "Select a country",
        list_countries)

    stats_country = df[df.country==country]

    if stats_country.shape[0]==1:
        col_numbers.write(stats_country.year.values[0])
        col_numbers.write(stats_country['count'].values[0])
    else:
        plotly_data = data = { 'type':'choropleth',
       'locations': stats_country,
       'locationmode': 'country names',
       'colorscale': 'viridis',
       'z':stats_country.groupby('country').mean().rate}
        col_numbers.plotly_chart(go.Figure(data=[data]))

    col_map.subheader("Average rate of homicides")


elif topic_box=='Suicide indicators':
    df = frames['suicide_100k']
    st.header('Suicide indicators')