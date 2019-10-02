from fondos_scraping import f_scraping
import db_mysql as dbmysql
import pandas as pd
from dotenv import load_dotenv
import os
import sentry_sdk

load_dotenv()
sentry_key = os.getenv("SENTRY_SDK")
sentry_sdk.init(sentry_key)
print("Connecting to -> {}".format(sentry_key))

full_path = os.path.realpath(__file__)
abs_path = os.path.dirname(full_path)[:-4]

def main(): 
    #Obtener nombre, ISIN y web de los fondos a scrapear
    fondos_master = pd.read_excel("{}/input/info_fondos.xlsx".format(abs_path),encoding='utf-8')
    fondos_master["FONDO"] = fondos_master["FONDO"].apply(lambda x: x.strip())
    
    #Llamar al web scraping: 
    #fondos_master = fondos_master.head(1)
    info_fondos = f_scraping(fondos_master)

    #Escribimos csv
    try:
        info_fondos.to_csv("{}/output/info_fondos.csv".format(abs_path),index= False)
    except Exception as e:
        print("Could not write info_fondos.csv. ", e)

    #Escribimos base de datos
    dbmysql.db_fondo(info_fondos)

    print("Info obtained!")

if __name__=="__main__":
    main()