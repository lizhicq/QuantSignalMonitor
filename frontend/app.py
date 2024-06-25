from flask import Flask, render_template, jsonify
from backend.StockPool import StockPool
from datetime import datetime
import glob,json,os

app = Flask(__name__)

def get_data():
    today_str = datetime.now().strftime("%Y%m%d")
    path = f'./data/leaderboard/{today_str}/*.json'
    list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r') as file:
        data = json.load(file)
    data = dict(data)
    for _window, stocks in data.items():
        for stock in stocks:
            stock['PriceIncrease'] = round(stock['PriceIncrease'], 2)
            stock['IntervalPriceIncrease'] = round(stock['IntervalPriceIncrease'], 2)
            stock['PriceSurge'] = round(stock['PriceSurge'], 2)
    return data

@app.route('/api/leaderboard')
def api_leaderboard():
    data = get_data()
    return jsonify(data)

@app.route('/leaderboard')
def leaderboard():    
    data = get_data()
    return render_template('leaderboard.html', leaderboard=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=True)
