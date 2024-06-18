# 用于从外部API获取数据
import requests,time
import pandas as pd
from config.data_config import API_CONFIG # type: ignore


def fetch_stock_ids(time=0):
    """
    Fetch stock ID definitions from the API.
    """
    params = {
        'sourceId': API_CONFIG['source_id'],
        'clientType': API_CONFIG['client_type'],
        'zip': API_CONFIG['zip'],
        'appId': API_CONFIG['app_id'],
        'time': time,
        'type': API_CONFIG['stock_id_type']
    }
    response = requests.get(API_CONFIG['base_url'], params=params)
    data = response.json()
    return pd.DataFrame(data['StockInfo'])

def get_update_stock_ids():
    return fetch_stock_ids(time.time())
    
def fetch_stock_data(stock_id, lasttime=0):
    """
    Fetch time-series data for a specific stock.
    """
    params = {
        'sourceId': API_CONFIG['source_id'],
        'lasttime': lasttime,
        'StockID': stock_id,
        'appId': API_CONFIG['app_id'],
        'type': API_CONFIG['time_series_type']
    }
    response = requests.get(API_CONFIG['base_url'], params=params)
    return response.json()

def get_update_stock_data(stock_id=84772085):
    init_data = fetch_stock_data(stock_id)
    last_call_epoch = init_data['Klineresult'][-1]['time'] 
    # 拉取时间，等于0，给出今天到当前时间的数据,后面用Klineresult最后一条time的时间获取增量数据
    update_Klineresult = fetch_stock_data(stock_id, lasttime=last_call_epoch)['Klineresult']
    return pd.DataFrame(update_Klineresult)

if __name__ == "__main__":
    #print(fetch_stock_ids())
    print(fetch_stock_data(16777218))
    #print(fetch_stock_data())