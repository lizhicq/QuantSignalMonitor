from backend.StockPool import StockPool
import pandas as pd
class LeaderBoard:
    
    def __init__(self):
        self.windows = [1,2,5,10,20,30]
        self.leaderboards = {}
        
        self.stock_pool = StockPool()
        self.stock_pool.update_stock_pool()
        
        self.top_stocks = {}
        self.rank = 20
        
    def update_top_stocks(self):
        all_top_stocks = set()
        for w in self.windows:
            last_w_min_top_stocks_id_set = set(
                self.stock_pool.last_n_min_top_m_stocks(n=w,m=self.rank))
            self.top_stocks[w] = last_w_min_top_stocks_id_set
            all_top_stocks |= last_w_min_top_stocks_id_set
        for stock_id in all_top_stocks:
            stock = self.stock_pool.total_pool[stock_id]
            stock.update_stock_klineres()
            
    def update_leaderboard(self):
        for window in self.windows:
            top_stock_ids = self.top_stocks[window]
            total_pool = self.stock_pool.total_pool
            data =  {
                'StockId': [total_pool[stock_id].wind_code for stock_id in top_stock_ids],
                'StockName': [total_pool[stock_id].name for stock_id in top_stock_ids],
                'TotalAmount': [total_pool[stock_id].last_n_min_total_amount(window) for stock_id in top_stock_ids],
                'PriceIncrease': [total_pool[stock_id].last_n_min_price_change_since_open(window) for stock_id in top_stock_ids],
                'IntervalPriceIncrease': [total_pool[stock_id].last_n_min_price_change_interval(window) for stock_id in top_stock_ids],
                'StatisticalInterval': [total_pool[stock_id].last_n_min_interval(window) for stock_id in top_stock_ids],
                'PriceSurge': [total_pool[stock_id].last_n_min_price_surge(window) for stock_id in top_stock_ids]
            }
            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by='TotalAmount', ascending=False)
            self.leaderboards[window] = df_sorted.to_json(orient='records',force_ascii=False)
