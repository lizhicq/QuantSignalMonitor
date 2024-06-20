from data_fetcher import *

stock_id_df = fetch_stock_ids()

stock_ids = set(stock_id_df['StockId'])

print(stock_ids)