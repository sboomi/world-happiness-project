import pandas as pd
from db import open_connection, close_connection

def standardize_table(filename, columns, standard_cols):
    df = pd.read_csv(filename, usecols=columns)
    df.columns = standard_cols
    return df

def run():
    common_list = ['country', 'freedom', 'economy', 'health', 'score', 'corruption', 'social_support', 'generosity']
    frames = []

    relevant_columns = {'2015': ['Country', 'Freedom', 'Economy (GDP per Capita)', 'Health (Life Expectancy)','Happiness Score', 'Trust (Government Corruption)', 'Family', 'Generosity'],
    '2016': ['Country', 'Freedom', 'Economy (GDP per Capita)', 'Health (Life Expectancy)','Happiness Score', 'Trust (Government Corruption)', 'Family', 'Generosity'],
    '2017': ['Country', 'Freedom', 'Economy..GDP.per.Capita.', 'Health..Life.Expectancy.','Happiness.Score', 'Trust..Government.Corruption.', 'Family', 'Generosity'],
    '2018': ['Country or region', 'Freedom to make life choices', 'GDP per capita', 'Healthy life expectancy','Score', 'Perceptions of corruption', 'Social support', 'Generosity'],
    '2019': ['Country or region', 'Freedom to make life choices', 'GDP per capita', 'Healthy life expectancy','Score', 'Perceptions of corruption', 'Social support', 'Generosity']}

    for year, cols in relevant_columns.items():
        filename = f"nbs/data/happy/{year}.csv"
        df = standardize_table(filename, cols, common_list)
        df['year'] = df.country.apply(lambda x: int(year))
        frames.append(df)

    happy = pd.concat(frames, ignore_index=True)

    # Register in database
    conn = open_connection()
    happy.to_sql('happy', con=conn, if_exists='replace')
    close_connection(conn)