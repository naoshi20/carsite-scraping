import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import re
import requests
import os
import csv

with open('contents.txt', 'r') as f:
    txt = f.read()

soup = BeautifulSoup(txt, "html.parser")

trs = soup.find_all("div", id=re.compile("tab01"))[0].find_all("table", class_=re.compile("tbl_distribution"))[0].find_all("tr")#[0]#.find_all(['th', 'td'])

rows = []
for (n,tr) in enumerate(trs):
    tx = tr.find_all(['th', 'td'])#[0]#.contents
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
            row.append(value)#.contents
        else:
            row.append(0)
    rows.append(row[1:])


jsonf = ".env/car-site-scraping-96e1530b4d88.json"
spread_sheet_key = "1pZJ0kHeguSslRHPkDkW8PtzEoXNu333Iaz6uslDzT48"


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key(spread_sheet_key)
worksheet = spreadsheet.get_worksheet(0)
worksheet.update('B2',rows[:22])

