import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import re
import requests
import os

url = 'https://www.goo-net.com/market/HONDA/10201043/'
path = './contents.txt'
f = open(path, 'w')

res = requests.get(url)
f.write(res.text)

f.close()