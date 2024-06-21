from backend.data_fetcher import *
from collections import deque
from concurrent.futures import ProcessPoolExecutor,as_completed
class Stock:
    def __init__(self, stock_id:int, name:str, wind_code:str) -> None:
        self.id = stock_id
        self.name = name
        self.wind_code = wind_code
        self.minute_amt = deque(maxlen=31)
        self.minute_data = deque(maxlen=31)

    def add_minute_data(self, record):
        """_summary_
        添加每分钟的交易量数据，并更新数据队列
        如果数据更新，则增加一条记录，否则不更新。 
        """
        if not self.minute_data or self.minute_data[-1] != record:
            self.minute_data.append(record)
            self.minute_amt.append(record['Amount'])
            
    def get_amt_of_last_n_minutes(self, n):
        """
        计算最近 n 分钟的累计交易量
        因为存储的是存量数据，需要做一次减法，需要n+1条数据
        """
        if len(self.minute_data) < n+1:
            return 0 # 如果没有足够数据，就默认成交金额是0
        return self.minute_amt[-1] - self.minute_amt[-1-n]
    
    def calculate_details(self):
        pass

    

if __name__ == "__main__":
    pass