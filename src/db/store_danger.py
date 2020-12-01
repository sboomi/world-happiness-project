import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
from db import open_connection, close_connection

def url_from_shortcut(filename):
    url = ''
    with open(filename, 'r') as file:
        for line in file.readlines():
            if "URL=" in line:
                url = line.replace("URL=", "")
    return url

def choose_table(soup, caption_content):
    chosen_table = None
    for table in soup.select('table'):
        if table.select_one('caption') and caption_content in table.select_one('caption').text:
            chosen_table = table
    return chosen_table


url_danger = url_from_shortcut('nbs/data/danger_dataset.url')
r = requests.get(url_danger).content
soup = BeautifulSoup(r, 'html.parser')
found_table = choose_table(soup, "Intentional homicide victims per 100,000 inhabitants.")

danger = pd.read_html(str(found_table))[2]
danger = danger.drop(['Region', 'Subregion'], axis=1)
danger.columns = ['country', 'rate', 'count', 'year']

# Register in database
conn = open_connection()
danger.to_sql('danger_100k', con=conn, if_exists='replace')
close_connection(conn)

