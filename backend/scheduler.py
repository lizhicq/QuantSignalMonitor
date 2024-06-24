import time
import signal
from datetime import datetime
from backend.StockPool import StockPool

stock_pool = StockPool()

class Scheduler:
    def __init__(self, interval):
        self.interval = interval
        self.running = True

    def update_leaderboard(self):
        try:
            stock_pool.update_stock_pool()
            stock_pool.create_leaderboard()
            StockPool.save_leaderboard(stock_pool.leaderboard)
            print(f'Stock pool got updated at {datetime.now()}')
        except Exception as e:
            print(f'Error updating stock pool: {e}')

    def start(self):
        while self.running:
            self.update_leaderboard()
            print(f'Waiting for next update in {self.interval} seconds')
            time.sleep(self.interval)

    def stop(self):
        self.running = False

def signal_handler(sig, frame):
    print('Received signal to stop scheduler')
    scheduler.stop()

if __name__ == "__main__":
    scheduler = Scheduler(20)
    signal.signal(signal.SIGINT, signal_handler)
    scheduler.start()