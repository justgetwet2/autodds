ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
fpath = "./fonts/Hiragino-Sans-GB-W3.ttf"
fprop = fm.FontProperties(fname=fpath, size=10)
import numpy as np
import pandas as pd
import pickle
import re
import requests


def get_soup(url):
    try:
        res = requests.get(url, headers=ua)
    except requests.RequestException as e:
        print("Error: ", e)
    else:
        return BeautifulSoup(res.content, "html.parser")

def get_dfs(url):
    dfs = []
    soup = get_soup(url)
    if soup:
        if soup.find("table"):
            dfs = pd.io.html.read_html(soup.prettify())
        else:
            print(f"It's no table! {url}")
    return dfs

def float_time(s):
    if ":" in s:
        a, b = s.split(":")
        ftime = int(a) * 60 + float(b)
    else:
        ftime = float(s)
    return ftime

def str_time(f):
    stime = ""
    if f:
        if f > 60.0:
            sec = f - 60.0
            stime = "1:" + str(round(sec, 1))
        elif f <= 60.0:
            stime = str(round(f, 1))
    return stime

def get_time(condition, stime):
    ftime = None
    if condition == "良":
        ftime = float_time(stime)
    if condition == "稍重":
        ftime = float_time(stime) + 0.2
    if condition == "重":
        ftime = float_time(stime) + 0.1
    return ftime

def left(digit, msg):
    import unicodedata
    for c in msg:
        digit -= 1
        if unicodedata.east_asian_width(c) in "FWA":
            digit -= 1
    return msg + ' '*digit

def times_for_boxplot(race):
    nankan_url =  "https://www.nankankeiba.com"
    yyyy = "2022"
    racename = " ".join(race[:5])
    print(racename)


if __name__ == "__main__":

    oddspark = "https://www.oddspark.com"
    autorace = oddspark + "/autorace"
    yyyy = "2022"

    placeCd_d = {'川口': '02', '伊勢崎': '03', '浜松': '04', '飯塚': '05', '山陽': '06'}
    placeEn_d = {'川口': 'kawaguchi', '伊勢崎': 'isesaki', '浜松': 'hamamatsu',\
                '飯塚': 'iizuka', '山陽': 'sanyo'}

    dt, place = "0625", "伊勢崎"
    races = []
    for raceNo in [str(n) for n in range(1,2)]:
        place_cd = placeCd_d[place]
        url = autorace + "/RaceList.do?" + f"raceDy={yyyy + dt}&placeCd={place_cd}&raceNo={raceNo}"
        soup = get_soup(url)

        dt_s = yyyy + "/" + dt[:2] + "/" + dt[2:]
        racename_tag = soup.select_one("#RCdata2 h3")
        racename = re.sub("\xa0", "", racename_tag.text.strip())
        dsc_tag = soup.select_one("#RCdata2 .RCdst")
        dsc = dsc_tag.text.split()
        wea, cnd, tmp = "天候", "走路状況", "走路温度"
        dsc_s = " ".join(s for s in dsc if s.startswith(wea) or s.startswith(cnd) or s.startswith(tmp))
        racetitle = dt_s + " " + place + " " +  str(raceNo).rjust(2, "0") + "R " + racename + " " + dsc_s
        print(racetitle)

        racer_tags = soup.select("td.hideElm a")
        for i, tag in enumerate(racer_tags):
            if i: continue
            print(tag.text)
            print(tag.get("href"))
            racer_url = oddspark + tag.get("href")
            df = get_dfs(racer_url)[-1]
            last_place, before_place = "", ""
            for j, row in df.iterrows():
                # if j: continue
                if j == 0:
                    last_place = row["開催場"]
                if not last_place == row["開催場"]:
                    print("spam spam spam")
                    before_place = row["開催場"]
                if not before_place == "" and not before_place == row["開催場"]:
                    last_place, before_place = "", ""
                if last_place or before_place:
                    print(last_place, before_place)
                    print(row["開催場"], row["走路\u0020\u0020(天候)"], row["競走T"])
            
    # filename = "./data/20220625_isesaki_data.pickle"
    # with open(filename, mode="rb") as f:
    #     races = pickle.load(f)

    # print(races[0][0])