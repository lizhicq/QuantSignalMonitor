import pandas as pd
from backend.Stock import Stock
from config.data_config import DATA_PATH_CONFIG
from backend.data_fetcher import *
import heapq,json

class StockPool:
    def __init__(self, stock_mapping_path=None):
        self.total_pool = {}
        if stock_mapping_path is None:
            stock_mapping_path = DATA_PATH_CONFIG['stock_mapping']
        df_mapping = pd.read_csv(stock_mapping_path,index_col='StockId')
        for StockId, row in df_mapping.iterrows():
            self.total_pool[StockId] = Stock(
                StockId, row['StockName'], row['WindCode'])
        
    def update_stock_pool(self, id_list=None):
        print('start to update stock pool general info....')
        if id_list is None:
            id_list = list(self.total_pool) # get keys
        records = []
        all_stock_general_data = {}
        for step in range(0, len(self.total_pool), 800):
            res = fetch_multi_stock_id(id_list[step:step+800])
            all_stock_general_data.update(res)
            records.extend(res['pk'])
        for record in records:
            self.total_pool[record['StokId']].add_minute_amt(record)
        print(f'finished query all stocks general info')
    
    def last_n_min_top_m_stocks(self, n, m):
        """
        返回过去n分钟交易量前m的股票id
        """
        top_stocks = heapq.nlargest(
            m,
            self.total_pool.items(),
            key=lambda item: item[1].get_amt_of_last_n_minutes(n)
        )
        return [item[0] for item in top_stocks]