from threading import Timer
from backend.data_processor import process_stock_data
from backend.data_fetcher import get_update_stock_ids
import pandas as pd

class Scheduler:
    def __init__(self, intervals):
        self.stock_info_df = get_update_stock_ids()
        self.intervals = intervals
        self.timer = None

def create_stock_pool():
    df = pd.read_csv("config/stock_mapping.csv")
    stock_pool = {}
    for row in df.iterrows():
        stock_pool[row['StockId']] = Stock(
            row['StockId'], row['StockName'], row['WindCode'])
    return stock_pool

def update_stock_pool(stock_pool:dict, id_list=None):
    if id_list is None:
        id_list = list(stock_pool) # get keys
    records = []
    for step in range(0, len(df), 800):
        res = fetch_multi_stock_id(id_list[step:step+800])
        records.extend(res['pk'])
    for record in records:
        stock_pool[record['StockId']].add_minute_data(record)
    def start(self):
        self.update_data()
        self.timer = Timer(3.0, self.start)
        self.timer.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()
