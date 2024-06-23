import pandas as pd
from backend.Stock import Stock
from datetime import datetime
from config.data_config import DATA_PATH_CONFIG
from backend.data_fetcher import fetch_multi_stock_id, fetch_single_stock_id
import heapq,json,os

class StockPool:
    def __init__(self, stock_mapping_path=None):
        if stock_mapping_path is None:
            stock_mapping_path = DATA_PATH_CONFIG['stock_mapping']
        self.mapping_df = pd.read_csv(stock_mapping_path,index_col='StockId')
        self.total_pool = {}
        for StockId, row in self.mapping_df.iterrows():
            self.total_pool[StockId] = Stock(
                StockId, row['StockName'], row['WindCode'])

    def update_stock_pool(self, id_list=None):
        if id_list is None:
            id_list = list(self.total_pool) # get keys
        records = []
        for step in range(0, len(self.total_pool), 800):
            res = fetch_multi_stock_id(id_list[step:step+800])
            records.extend(res['pk'])
        for record in records:
            self.total_pool[record['StockId']].add_minute_data(record)
            
    def get_top_amt_stocks(self, window, num):
        """
        返回区间内前交易额前20的股票
        """
        return heapq.nlargest(
            num,
            self.total_pool.items(),
            key=lambda item: item[1].get_amt_of_last_n_minutes(window)
        )
        
    def create_leaderboard(self, top_num=10):
        windows = [1, 2, 3, 5, 10, 20, 30]
        self.leaderboard = {}
        for window in windows:
            results = []
            for stock_id, stock in self.get_top_amt_stocks(window, top_num):
                try:
                    res = fetch_single_stock_id(stock_id)
                    df = pd.DataFrame(res['Klineresult'])
                    df_roll = df.iloc[-window:]
                except Exception as e:
                    print(f"Got Exception on {stock_id}, Exception is {e}")
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
                    'PriceIncrease': price_increase,# 涨幅（Price Increase） - 10分钟结束时的收盘价与开始时的开盘价之差。
                    'IntervalPriceIncrease': interval_price_increase,# 区间涨幅（Interval Price Increase） - 10分钟内最高价与最低价之差。
                    'StatisticalInterval': statistical_interval, # 统计区间（Statistical Interval） - 选择的10分钟内数据点的时间范围。
                    'PriceSurge': price_surge # 拉升幅度（Price Surge） - 最低价到最高价的涨幅比例。
                })
            self.leaderboard[window] = results  # Correct key usage for different windows
        self.save_leaderboard()
        return json.dumps(self.leaderboard, ensure_ascii=False)  # Convert dictionary to JSON string`

    def save_leaderboard(self):
        """保存当前leaderboard到一个按时间命名的JSON文件中"""
        base_dir = DATA_PATH_CONFIG['leaderboard_saving_path']
        current_time = datetime.now()
        date_path = current_time.strftime('%Y%m%d')
        time_path = current_time.strftime('%H:%M')
        full_path = os.path.join(base_dir, date_path)
        os.makedirs(full_path, exist_ok=True)
        file_name = f"{time_path}.json"
        full_file_path = os.path.join(full_path, file_name)

        # 假设 self.leaderborad 是已经生成的数据
        with open(full_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.leaderboard, f, ensure_ascii=False)

        return full_file_path
