import pandas as pd
from backend.Stock import Stock
from backend.data_fetcher import fetch_multi_stock_id

class StockPool:
    def __init__(self, stock_mapping_path=None):
        if stock_mapping_path is None:
            stock_mapping_path = "config/stock_mapping.csv"
        df = pd.read_csv(stock_mapping_path)
        self.total_pool = {}
        for row in df.iterrows():
            self.total_pool[row['StockId']] = Stock(
                row['StockId'], row['StockName'], row['WindCode'])

    def update_stock_pool(self, id_list=None):
        if id_list is None:
            id_list = list(self.total_pool) # get keys
        records = []
        for step in range(0, len(self.total_pool), 800):
            res = fetch_multi_stock_id(id_list[step:step+800])
            records.extend(res['pk'])
        for record in records:
            self.total_pool[record['StockId']].add_minute_data(record)