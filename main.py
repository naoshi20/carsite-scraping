import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import re
import requests
import os
import csv
import datetime
import pytz

#start-scraping
cars = [{"url":"https://www.goo-net.com/market/HONDA/10201043/","type_":"S660","model":["2015","2016","2017","2018","2019","2020","2021","2022"]},{"url":"https://www.goo-net.com/market/NISSAN/10151010/","type_":"スカイライン","model":["2008","2009","2010","2011","2012","2013"]},{"url":"https://www.goo-net.com/market/TOYOTA/10101004/","type_":"クラウンアスリート","model":["2008","2009","2010","2011","2012","2013"]}]

#jsonf = "/.env/car-site-scraper" #production
jsonf = "./.env/car-site-scraping-96e1530b4d88.json" #local
spread_sheet_key = "***"
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

for j in range(len(cars)):
    res = requests.get(cars[j]["url"])

    soup = BeautifulSoup(res.text, "html.parser")

    trs = soup.find_all("div", id=re.compile("tab01"))[0].find_all("table", class_=re.compile("tbl_distribution"))[0].find_all("tr")

    rows = []
    for (n,tr) in enumerate(trs):
        tx = tr.find_all(['th', 'td'])
        row = []
        if n == 0:
            continue
        for td in tx:
            a = td.find_all("a")
            if len(a) > 0:
                try:
                    value = int(a[0].text.replace("\n","").replace(" ",""))
                except:
                    value = 0
                row.append(value)
            else:
                row.append(0)
        rows.append(row[1:])

    #authorization
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)

    #get-spreadsheet
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open_by_key(spread_sheet_key)
    
    try:
        worksheet = spreadsheet.worksheet(cars[j]["type_"])
    
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=cars[j]["type_"], rows="25", cols="20")

    #update-sheet
    worksheet.update('B2',rows[:22])

    for i in range(len(cars[j]["model"])):
        title = cars[j]["type_"] + "_" + cars[j]["model"][i]
        try:
            worksheet2 = spreadsheet.worksheet(title)

        except gspread.exceptions.WorksheetNotFound:
            worksheet2 = spreadsheet.add_worksheet(title=title, rows="25", cols="20")

        now = [str(datetime.datetime.today())]

        df = pd.DataFrame(worksheet.get_all_records())
        print(df)

        row = df.loc[:,cars[j]["model"][i]].values.tolist()
        price = df.loc[:,"価格"].values.tolist()[2:21]
        sum = 0

        for k in range(len(row[2:21])):
            sum += int(price[k]) * int(row[2:21][k])
        try:
            avg = sum / row[0]
        except ZeroDivisionError:
            avg = 0

        row = now + list(reversed(row)) + [avg]

        print(row)
        spreadsheet.values_append(title,
                        {'valueInputOption': 'USER_ENTERED'},
                        {'values': [row]})
