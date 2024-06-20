from threading import Timer
from data_processor import process_stock_data
from data_fetcher import get_update_stock_ids

class Scheduler:
    def __init__(self, intervals):
        self.stock_info_df = get_update_stock_ids()
        self.intervals = intervals
        self.timer = None

    def update_data(self):
        """
        Fetch and update stock data, then regenerate leaderboards.
        """
        stocks = self.stock_data_fetcher.fetch_stocks()  # This should fetch and update stock objects
        leaderboards = process_stock_data(stocks, self.intervals)
        # Here you could update a database or in-memory data structure with the leaderboards

    def start(self):
        self.update_data()
        self.timer = Timer(3.0, self.start)
        self.timer.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()
