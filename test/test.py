from backend.StockPool import StockPool
from flask import jsonify
stock_pool = StockPool()
lb = stock_pool.create_leaderboard()
print(lb)
