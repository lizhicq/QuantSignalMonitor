# 用于从外部API获取数据
import requests,json,os
from datetime import datetime
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
    print(f'Debug: single stock query is called url={response.url}')
    if single_stock_res and single_stock_res['state'] == 0 and len(single_stock_res['Klineresult']) > 1:
        return single_stock_res

def save_json_to_datetime_path(json_data, base_dir):
    """_summary_
    保存json数据到base_dir下的按日期命名的文件夹,分钟命名的文件里面
    """
    current_time = datetime.now()
    date_path = current_time.strftime('%Y%m%d')
    time_path = current_time.strftime('%H-%M')
    full_path = os.path.join(base_dir, date_path)
    os.makedirs(full_path, exist_ok=True)
    file_name = f"{time_path}.json"
    full_file_path = os.path.join(full_path, file_name)

    # 假设 json_data 是已经生成的数据
    with open(full_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    return full_file_path

if __name__ == "__main__":
    pass