import pandas as pd
from data_fetcher import *
import concurrent.futures
import multiprocessing
import time as time_module
class Stock:
    def __init__(self, stock_id, name):
        self.stock_id = stock_id
        raw_data = fetch_stock_data(self.stock_id)
        self.stock_info_df = pd.DataFrame(raw_data)


if __name__ == "__main__":
    stock_id_df = fetch_stock_ids()
    x_set = set(stock_id_df['StockId'])
    x_list = list(x_set)
    # 使用 ThreadPoolExecutor 来创建线程池
    start = time_module.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交所有任务并获取 future 对象
        futures = [executor.submit(fetch_stock_data, x) for x in x_list]
        # as_completed 生成器在每个 future 完成时产生 future
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result()  # 获取任务结果
            print(f'任务 {i}/{len(x_list)} 完成')
    end = time_module.time()
    print('time comsuption:')
    print(end - start)
        