import pymysql
from sqlalchemy import create_engine

#environment:
MYSQL_DATABASE='WH_docker'
MYSQL_USER= 'sboomi'
MYSQL_PASSWORD= 'sboomi'
MYSQL_ROOT_PASSWORD= 'root2020'
host="127.0.0.1:3306" #'0.0.0.0:3306'

DATABASE_URI= "mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=MYSQL_USER,host=host,pw=MYSQL_PASSWORD,db=MYSQL_DATABASE)

def open_connection(uri=DATABASE_URI):
    engine = create_engine(uri)
    return engine

def close_connection(engine):
    engine.dispose()