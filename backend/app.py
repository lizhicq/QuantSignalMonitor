from flask import Flask
from scheduler import Scheduler
from some_module import StockDataFetcher  # Placeholder for your actual data fetching class

app = Flask(__name__)
scheduler = Scheduler(StockDataFetcher(), intervals=[60, 120, 300, 600, 1200, 1800])

@app.route('/start')
def start():
    scheduler.start()
    return "Scheduler started!"

@app.route('/stop')
def stop():
    scheduler.stop()
    return "Scheduler stopped!"
