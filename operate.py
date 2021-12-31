import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime
import pytz


jsonf = ".env/car-site-scraping-96e1530b4d88.json"
spread_sheet_key = "1pZJ0kHeguSslRHPkDkW8PtzEoXNu333Iaz6uslDzT48"

cars = [{"type_":"S660","model":["2017","2018","2019","2020","2020以上"]}]

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key(spread_sheet_key)

try:
    worksheet = spreadsheet.worksheet(cars[0]["type_"])

except gspread.exceptions.WorksheetNotFound:
    worksheet = spreadsheet.add_worksheet(title=cars[0]["type_"], rows="1", cols="15")

for i in range(len(cars[0]["type_"])):
    title = cars[0]["type_"] + "_" + cars[0]["model"][i]
    try:
        worksheet2 = spreadsheet.worksheet(title)

    except gspread.exceptions.WorksheetNotFound:
        worksheet2 = spreadsheet.add_worksheet(title=title, rows="1", cols="15")

    now = [str(datetime.datetime.today())]

    df = pd.DataFrame(worksheet.get_all_records())
    print(df)

    row = df.loc[:,cars[0]["model"][i]].values.tolist()
    row = now + list(reversed(row))

    print(row)
    spreadsheet.values_append(title,
                    {'valueInputOption': 'USER_ENTERED'},
                    {'values': [row]})