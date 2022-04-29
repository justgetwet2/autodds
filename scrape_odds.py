ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd
import re
import requests

url_oddspark = "https://www.oddspark.com/autorace"

placeCd_d = {'川口': '02', '伊勢崎': '03', '浜松': '04', '飯塚': '05', '山陽': '06'}
placeEn_d = {'川口': 'kawaguchi', '伊勢崎': 'isesaki', '浜松': 'hamamatsu',\
            '飯塚': 'iiduka', '山陽': 'sanyo'}

def get_dfs(url):
    res = requests.get(url, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    dfs = []
    if soup.find("table"):
        dfs = pd.io.html.read_html(soup.prettify())
    else:
        print(f"it's no table! {url}")
    return dfs

def get_meta(dt, place, entry_url):
    dt_s = dt[:4] + "/" + dt[4:6] + "/" + dt[6:]
    meta = [dt_s, place]
    res = requests.get(entry_url, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    tag = soup.select_one("#RCdata1 span")
    r = tag.text.strip("R")
    tag = soup.select_one("#RCdata2 h3")
    dsc = re.sub("\xa0", "", tag.text.strip())
    meta += [r, dsc]
    tags = soup.select("#RCdata2 .RCdst")
    items = tags[0].text.split()
    meta += [item for item in items if item.startswith("天候") or item.startswith("走路状況")]

    return meta

def onerace(dt, place, raceNo):

    place_cd = placeCd_d[place]
    race_url = f"raceDy={dt}&placeCd={place_cd}&raceNo={raceNo}"

    entry_url = url_oddspark + "/RaceList.do?" + race_url

    win_place_url = url_oddspark + "/Odds.do?" + race_url + "&betType=1&viewType=0"
    quinella_url = url_oddspark + "/Odds.do?" + race_url + "&betType=6&viewType=0"
    exacta_url = url_oddspark + "/Odds.do?" + race_url + "&betType=5&viewType=0"
    wide_url = url_oddspark + "/Odds.do?" + race_url + "&betType=7&viewType=0"
    trio_url = url_oddspark + "/Odds.do?" + race_url + "&betType=9&viewType=0" 
    
    odds_urls = [win_place_url, quinella_url, exacta_url, wide_url, trio_url]
    
    trifecta_url = url_oddspark + "/Odds.do?" + race_url + "&viewType=0&betType=8"

    dfs = get_dfs(entry_url)
    if dfs:
        entry_df = dfs[-1]
        bikes =  [str(n) for n in range(1, len(entry_df)+1)]
    else:
        print("no entry!")
        return []

    meta = get_meta(dt, place, entry_url)

    odds = []
    for url in odds_urls:
        dfs = get_dfs(url)
        odds.append(dfs)

    # raceNo=7&viewType=0&betType=8&bikeNo=1&jikuNo=1
    trifectas = []
    for bike in bikes:
        trifecta_bike_url = trifecta_url + f"&bikeNo={bike}&jikuNo=1"
        dfs = get_dfs(trifecta_bike_url)
        trifectas.append(dfs)

    return [meta, entry_df, odds, trifectas]


def odds_dict(dt, place, raceNo):
    race = onerace(dt, place, raceNo)
    print(race[0])
    winplace_df = race[2][0][0]
    quinella_df = race[2][1][2]
    exacta_df = race[2][2][2]
    wide_df = race[2][3]
    trio_df = race[2][4]
    trifs = race[3]
    
    odds_d = {}

    for t in winplace_df.itertuples():
        odds_d[str(t.車番)] = t.単勝オッズ

    for i, t in enumerate(quinella_df.itertuples()):
        for j, v in enumerate(t[2::2]):
            s = str(j+1) + "=" + str(j+i+2)
            if not np.isnan(v):
                odds_d[s] = v

    for i, t in enumerate(exacta_df.itertuples()):
        if i > 1:
            for j, v in enumerate(t[3:]):
                value = float(v)
                if not np.isnan(value):
                    s = str(j+1) + "-" + str(i-1)
                    odds_d[s] = value

    for trif in trifs:
        for df in trif[2:]:
            for t in df.itertuples():
                s = "".join(t.車番.replace("→", "-").split())
                odds_d[s] = t.オッズ

    return odds_d


if __name__=='__main__':

    # dt = datetime.now().strftime("%Y%m%d")
    dt = "20220413"
    place = "山陽"
    r = 8

    odds_d = odds_dict(dt, place, r)
    bets = "1", "2", "3-4", "3-7", "4-7"
    for bet in bets:
        print(odds_d[bet])
