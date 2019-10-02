from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
mysql_password = os.getenv("MYSQL_PASSWORD")


def db_fondo(df):
    date_name = 'fondos_'+ str(max(pd.to_datetime(df.fecha_act.dropna())).date()).replace("-","")
    connect_and_write(df,date_name)


def connect_and_write(df,table_name):
    sqlEngine = create_engine('mysql+pymysql://root:{}@localhost/val'.format(mysql_password))
    dbConnection = sqlEngine.connect()
    try:
        frame = df.to_sql(table_name, dbConnection, if_exists="fail")
        print("MySQL data transfer succesfull!")
    except Exception as e:
        print(e)
    dbConnection.close()

