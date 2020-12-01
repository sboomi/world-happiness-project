import pandas as pd
from db import open_connection, close_connection

suicide = pd.read_csv("nbs/data/suicide_dataset.csv")

suicide_100k = suicide[['Country', 'Sex', 'Year', 'Suicide Rate']]
suicide_100k.columns = ["_".join(column.lower().split()) for column in suicide_100k.columns.values]

conn = open_connection()
suicide_100k.to_sql('suicide_100k', con=conn, if_exists='replace')
close_connection(conn)