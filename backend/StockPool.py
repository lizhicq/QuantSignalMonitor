import pandas as pd
from backend.Stock import Stock
from config.data_config import DATA_PATH_CONFIG
from backend.data_fetcher import fetch_multi_stock_id, fetch_single_stock_id
import heapq

class StockPool:
    def __init__(self, stock_mapping_path=None):
        if stock_mapping_path is None:
            stock_mapping_path = DATA_PATH_CONFIG['stock_mapping']
        df = pd.read_csv(stock_mapping_path)
        self.total_pool = {}
        for _, row in df.iterrows():
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
            
    def get_top_amt_stocks(self, window, num):
        """
        返回区间内前交易额前20的股票
        """
        return heapq.nlargest(
            num,
            self.total_pool.items(),
            key=lambda item: item[1].get_amt_of_last_n_minutes(window)
        )
        
    def create_leaderboard(self):
        window = 5
        results = []
        for stock_id, _amt in self.get_top_amt_stocks(window, 50):
            res = fetch_single_stock_id(stock_id)
            df = pd.DataFrame(res['Klineresult'])
            df_roll = df.rolling(window=window, on='time')
            # 成交金额（Total Amount） - 10分钟内所有交易的成交金额总和。
            # 涨幅（Price Increase） - 10分钟结束时的收盘价与开始时的开盘价之差。
            # 区间涨幅（Interval Price Increase） - 10分钟内最高价与最低价之差。
            # 统计区间（Statistical Interval） - 选择的10分钟内数据点的时间范围。
            # 拉升幅度（Price Surge） - 最低价到最高价的涨幅比例。
            # 计算各项指标
            total_amount = df_roll['Amount'].sum()
            price_increase = df_roll['Close'].apply(lambda x: x.iloc[-1]) - df_roll['Open'].apply(lambda x: x.iloc[0])
            statistical_interval = df_roll['time'].apply(lambda x: x.max() - x.min())

            range_high, range_low = df_roll['High'].max(), df_roll['Low'].min()
            interval_price_increase = range_high - range_low
            price_surge = (range_high - range_low) /range_low
            # 存储结果
            results[window] = {
                'Total Amount': total_amount,
                'Price Increase': price_increase,
                'Interval Price Increase': interval_price_increase,
                'Statistical Interval': statistical_interval,
                'Price Surge': price_surge
            }

# 展示结果，例如10分钟窗口
