from backend.data_fetcher import *
from collections import deque
import time

class Stock:
    def __init__(self, stock_id:int, stock_name:str, wind_code:str) -> None:
        self.id = stock_id
        self.name = stock_name
        self.wind_code = wind_code
        self.minute_amt = deque(maxlen=31)
        self.minute_data = deque(maxlen=31)
        self.klineres = None
        
    def add_minute_amt(self, record):
        """_summary_
        添加每分钟的交易量数据，并更新数据队列
        如果数据更新，则增加一条记录，否则不更新。 
        """
        if not self.minute_data or self.minute_data[-1] != record:
            self.minute_amt.append(record['Amount'])
            
    def get_amt_of_last_n_minutes(self, n):
        """
        计算最近 n 分钟的累计交易量
        因为存储的是存量数据,需要做一次减法,需要n+1条数据
        """
        if len(self.minute_amt) < n+1:
            return self.minute_amt[-1] # 如果没有足够数据，就默认成交金额是最后一项
        return self.minute_amt[-1] - self.minute_amt[-1-n]
    
    def update_stock_klineres(self):
        response = fetch_single_stock_id(self.id)
        self.klineres = pd.DataFrame(response['Klineresult'])
        
    def last_n_min_total_amount(self, n:int):
        df = self.klineres.iloc[-n:]
        return df['Amount'].sum()
    
    def last_n_min_price_change_since_open(self, n:int):
        open = self.klineres.iloc[0]['Open']
        close = self.klineres.iloc[-1]['Close']
        return (close - open)/open
    
    def last_n_min_price_change_interval(self, n:int):
        open = self.klineres.iloc[-n]['Open']
        close = self.klineres.iloc[-1]['Close']
        return (close - open)/open
    
    def last_n_min_interval(self, n:int):
        start = time.localtime(self.klineres.iloc[-n]['time'])
        end = time.localtime(self.klineres.iloc[-1]['time'])
        fstart = time.strftime("%H:%M", start)
        fend = time.strftime("%H:%M", end)
        return f"{fstart} - {fend}"
        
    def last_n_min_price_surge(self, n:int):
        df = self.klineres.iloc[-n:]
        running_low, price_surge = float('inf'), 0
        for _index, row in df.iterrows():
            running_low = min(running_low, row['Low'])
            price_surge = max((row['High']-running_low)/running_low, price_surge)
        return price_surge

if __name__ == "__main__":
    pass