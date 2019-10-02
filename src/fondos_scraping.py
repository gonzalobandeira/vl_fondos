import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from sentry_sdk import capture_exception


def rent_to_float(x):
    # noinspection PyBroadException
    try:
        return float(x) / 100
    except Exception:
        return x


def info_fondo(soup):

    table = soup.select("#overviewQuickstatsDiv > table")  # Tabla info fondo
    table_2 = soup.select("#overviewCalenderYearReturnsDiv > table")  # Table info rentabilidades pasadas

    fondo = {}
    # Generamos toda la info de sobre el fondo que nos interesa.
    try:
        fondo["name"] = re.sub(" +", " ",
                               re.sub("\n", "", soup.select("div[class=snapshotTitleBox] h1")[0].text.strip("\n, ,$")))

        row = table[0].findAll("tr")

        vl = row[1].findAll("td")
        fondo["fecha_act"] = re.sub(r"\.", "/", re.findall(r"\d+[./]\d+[./]\d+", vl[0].text)[0])
        fondo["vl"] = float(re.sub(r",", ".", re.findall(r"\d+[.,]?\d+", vl[2].text)[0]))
        fondo["moneda"] = re.findall(r"[A-Z]+", vl[2].text)[0]

        v_d = row[2].findAll("td")
        fondo["var_dia_%"] = re.sub(r",", ".", v_d[2].text.strip("\n, ,%"))
        if fondo["var_dia_%"] != "-":
            fondo["var_dia_%"] = float(fondo["var_dia_%"]) / 100

        v_c = row[3].findAll("td")
        fondo["cat"] = v_c[2].text

        v_i = row[4].findAll("td")
        fondo["ISIN"] = v_i[2].text

        # Rentabilidades a lo largo de los años
        # noinspection NonAsciiCharacters
        r_años = table_2[0].findAll("td")
        fondo["2015"] = rent_to_float(re.sub(",", ".", r_años[2].text))
        fondo["2016"] = rent_to_float(re.sub(",", ".", r_años[3].text))
        fondo["2017"] = rent_to_float(re.sub(",", ".", r_años[4].text))
        fondo["2018"] = rent_to_float(re.sub(",", ".", r_años[5].text))
        fondo["2019"] = rent_to_float(re.sub(",", ".", r_años[6].text))

    except Exception as e:
        print("Found error obtaining its data", Exception, e)
        capture_exception(e)

    return fondo


def f_scraping(df):
    fondos = []
    cookies = {
        "_evidon_consent_cookie": '{"consent_date":"' + str(date.today()) + 'T07:07:07.777Z"}',
        # cookies para pop-up MorningStar
    }

    for index, row in df.iterrows():
        print("{}. Getting info from {}".format(index + 1, row[1]))

        page = requests.get(row[2], cookies=cookies)

        soup = BeautifulSoup(page.text, "html.parser")
        fondos.append(info_fondo(soup))
        df_fondos = pd.DataFrame(fondos).dropna()

    return df_fondos[["ISIN", "name", "fecha_act", "vl", "moneda", "var_dia_%", "2015", "2016", "2017", "2018", "2019", "cat"]]


if __name__ == "__main__":
    fondos_master = pd.read_excel("input/info_fondos.xlsx")
    f_scraping(fondos_master)
