import pandas as pd
from backend.Stock import Stock
from config.data_config import DATA_PATH_CONFIG
from backend.data_fetcher import *
import heapq,json

class StockPool:
    def __init__(self, stock_mapping_path=None):
        if stock_mapping_path is None:
            stock_mapping_path = DATA_PATH_CONFIG['stock_mapping']
        self.mapping_df = pd.read_csv(stock_mapping_path,index_col='StockId')
        self.total_pool = {}
        self.top_stocks = {}
        self.leaderboard = {}
        for StockId, row in self.mapping_df.iterrows():
            self.total_pool[StockId] = Stock(
                StockId, row['StockName'], row['WindCode'])
        
    def update_stock_pool(self, id_list=None):
        print('this method is called ')
        if id_list is None:
            id_list = list(self.total_pool) # get keys
        records = []
        savd_data = {}
        for step in range(0, len(self.total_pool), 800):
            res = fetch_multi_stock_id(id_list[step:step+800])
            savd_data.update(res)
            records.extend(res['pk'])
        save_json_to_datetime_path(savd_data,DATA_PATH_CONFIG['stockpool_saving_path'])
        print(f'stock pool is saved')
        for record in records:
            self.total_pool[record['StokId']].add_minute_data(record)
    
            
    def get_top_amt_stocks(self, window, num):
        """
        返回区间内前交易额前num的股票
        """
        return heapq.nlargest(
            num,
            self.total_pool.items(),
            key=lambda item: item[1].get_amt_of_last_n_minutes(window)
        )
    
    def update_top_amt_stocks(self):
        for window in [1,2,3,5,10,20,30]:
            top_50 = self.get_top_amt_stocks(window, 50)
            self.top_stocks[window] = top_50
        
    def create_leaderboard(self, top_num=50):
        windows = [1, 2, 3, 5, 10, 20, 30]
        for window in windows:
            results = []
            for stock_id, stock in self.get_top_amt_stocks(window, top_num):
                try:
                    res = fetch_single_stock_id(stock_id)
                    df = pd.DataFrame(res['Klineresult'])
                    df_roll = df.iloc[-window:].sort_values(by=['Amount'])
                except Exception as e:
                    print(f"Got Exception during create leaderboard on {stock_id} and stock={stock.name}, Exception is {e}")
                    continue
                # Calculate metrics
                total_amount = int(df_roll['Amount'].sum())  # Convert to int
                price_increase = float(df_roll['Close'].iloc[-1] - df_roll['Open'].iloc[0])  # Convert to float
                statistical_interval = int(df_roll['time'].max() - df_roll['time'].min())  # Convert to int
                
                range_high, range_low = df_roll['High'].max(), df_roll['Low'].min()
                interval_price_increase = float(range_high - range_low)  # Convert to float
                if range_low != 0:
                    price_surge = float((range_high - range_low) / range_low)  # Convert to float
                else:
                    price_surge = float('inf')  # Handle division by zero
                # Store results
                results.append({
                    'StockId': stock_id,
                    'StockName': stock.name,
                    'TotalAmount': total_amount,# 成交金额（Total Amount） - 10分钟内所有交易的成交金额总和。
                    'PriceIncrease': price_increase,# 涨幅（Price Increase） - 当天开盘价
                    'IntervalPriceIncrease': interval_price_increase,# 区间收盘到开盘
                    'StatisticalInterval': statistical_interval, # 统计区间（Statistical Interval） - 选择的10分钟内数据点的时间范围。
                    'PriceSurge': price_surge # 拉升幅度（Price Surge） - 最低价到最高价的涨幅比例。
                })
            self.leaderboard[window] = results  # Correct key usage for different windows
        return json.dumps(self.leaderboard, ensure_ascii=False)  # Convert dictionary to JSON string`
    
    def save_leaderboard(self,base_dir=DATA_PATH_CONFIG['leaderboard_saving_path']):
        return save_json_to_datetime_path(
            self.leaderboard,
            base_dir
        )
