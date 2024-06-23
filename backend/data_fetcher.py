# 用于从外部API获取数据
import requests
import pandas as pd
from config.data_config import * # type: ignore

def fetch_multi_stock_id(stock_ids):
    stock_ids_str = ','.join(map(str,stock_ids))
    # 构建请求URL，直接包含所有参数
    # Bug fix, requests.get(API_CONFIG['base_url'], params=params) 会把‘,’转成 %2C
    request_url = (
        f"{MULTI_API_CONFIG['base_url']}?"
        f"sourceId={MULTI_API_CONFIG['sourceId']}&"
        f"refreshSource={MULTI_API_CONFIG['refreshSource']}&"
        f"StockID={stock_ids_str}&"  # 直接在URL中构建，避免自动编码
        f"clientType={MULTI_API_CONFIG['clientType']}&"
        f"appId={MULTI_API_CONFIG['appId']}&"
        f"imei={MULTI_API_CONFIG['imei']}&"
        f"deviceNo={MULTI_API_CONFIG['deviceNo']}&"
        f"packageName={MULTI_API_CONFIG['packageName']}&"
        f"type={MULTI_API_CONFIG['type']}&"
        f"version={MULTI_API_CONFIG['version']}"
    )

    # 发送GET请求
    retry = 0
    while retry < 5:
        try:
            response = requests.get(request_url)
            result = response.json()
            print(f"Debug Info: query multi stock ids URI {response.url},retry={retry}")
            return result
        except Exception as e:  # 包括处理JSON解码失败的情况
            print(e)
            retry += 1
    return None

def fetch_all_stock_info(lasttime=0):
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
    print(f"Debug Info: all stock info URI{response.url}")
    if stock_result and stock_result['state'] == 0:
        return pd.DataFrame(stock_result['StockInfo'])
    
def fetch_single_stock_id(stock_id:int, lasttime=0):
    """
    Fetch time-series data for a specific stock.
    """
    params = {
        'sourceId': API_CONFIG['source_id'],
        'lasttime': lasttime,
        'StockID': str(stock_id),
        'appId': API_CONFIG['app_id'],
        'type': API_CONFIG['time_series_type']
    }
    response = requests.get(API_CONFIG['base_url'], params=params)
    single_stock_res = response.json()
    if single_stock_res and single_stock_res['state'] == 0 and len(single_stock_res['Klineresult']) > 1:
        return single_stock_res

if __name__ == "__main__":
    pass