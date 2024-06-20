# 用于从外部API获取数据
import requests
import pandas as pd
from config.data_config import * # type: ignore

def fetch_stocks():
    df = pd.read_csv("config/stock_mapping.csv")
    for step in range(0, len(df), 1000):
        ids_set = df.iloc[step:step+1000]['StockId'].apply(str)
        ids_list = ','.join(ids_set)
        res = fetch_stock_id_amt(ids_list)
        print(res)
    return

def fetch_stock_id_amt(stock_ids:list):
    params = {
        "sourceId": MULTI_API_CONFIG['sourceId'],
        "refreshSource": MULTI_API_CONFIG['refreshSource'],
        "StockID": ','.join(stock_ids),
        "clientType": MULTI_API_CONFIG['clientType'],
        "appId":MULTI_API_CONFIG['appId'],
        "imei": MULTI_API_CONFIG['imei'],
        "deviceNo": MULTI_API_CONFIG['deviceNo'],
        "packageName": MULTI_API_CONFIG['packageName'],
        "type": MULTI_API_CONFIG['type'],
        "version": MULTI_API_CONFIG['version']
    }
    ç = requests.get(MULTI_API_CONFIG['base_url'], params=params)
    result = response.json()
    return result

def fetch_stock_ids(lasttime=0):
    """
    Fetch stock ID definitions from the API.
    """
    params = {
        'sourceId': API_CONFIG['source_id'],
        'clientType': API_CONFIG['client_type'],
        'zip': API_CONFIG['zip'],
        'appId': API_CONFIG['app_id'],
        'time': lasttime,
        'type': API_CONFIG['stock_id_type']
    }
    response = requests.get(API_CONFIG['base_url'], params=params)
    stock_result = response.json()
    if stock_result and stock_result['state'] == 0:
        return pd.DataFrame(stock_result['StockInfo'])
    
def fetch_stock_data(stock_ids:str, lasttime=0):
    """
    Fetch time-series data for a specific stock.
    """
    params = {
        'sourceId': API_CONFIG['source_id'],
        'lasttime': lasttime,
        'StockID': stock_ids,
        'appId': API_CONFIG['app_id'],
        'type': API_CONFIG['time_series_type']
    }
    response = requests.get(API_CONFIG['base_url'], params=params)
    stock_info_res = response.json()
    
   # print(stock_id, stock_info_res)
    if stock_info_res and stock_info_res['state'] == 0 and len(stock_info_res['Klineresult']) > 1:
        return stock_info_res['Klineresult']

if __name__ == "__main__":
    fetch_stocks()