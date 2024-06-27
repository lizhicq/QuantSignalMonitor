from flask import Flask, render_template, jsonify
from datetime import datetime
import glob,json,os


today_str = datetime.now().strftime("%Y%m%d")
path = f'./data/leaderboard/{today_str}/*.json'
list_of_files = glob.glob(path)
latest_file = max(list_of_files, key=os.path.getctime)
with open(latest_file, 'r') as file:
    data = json.load(file)
data = dict(data)
for _window, stocks_str in data.items():
    stocks = json.loads(stocks_str)
    for stock in stocks:
        stock['PriceIncrease'] = round(stock['PriceIncrease'], 2)
        stock['IntervalPriceIncrease'] = round(stock['IntervalPriceIncrease'], 2)
        stock['PriceSurge'] = round(stock['PriceSurge'], 2)