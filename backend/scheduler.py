import time
from datetime import datetime,time as dtime
from backend.LeaderBoard import LeaderBoard
from backend.data_fetcher import save_json_to_datetime_path
from config.data_config import DATA_PATH_CONFIG
class Scheduler:
    def __init__(self, interval):
        self.interval = interval
        self.running = True

    def update(self):
        try:
            leaderboard = LeaderBoard()
            leaderboard.update_top_stocks()
            leaderboard.update_leaderboard()
            print(f'LeaderBoard got updated at {datetime.now()}')
            
            save_json_to_datetime_path(
                leaderboard.leaderboards,
                DATA_PATH_CONFIG['leaderboard_saving_path']
            )
            print(f'LeaderBoard got saved at {datetime.now()}')
        except Exception as e:
            print(f'Error updating stock pool: {e}')

    def start(self):
        while self.running:
            now = datetime.now().time()
            # Check if current time is within 11:30 to 13:30
            # if dtime(11, 30) <= now <= dtime(13, 30):
            #     wait_time = (dtime(13, 30).hour * 3600 + dtime(13, 30).minute * 60) - (now.hour * 3600 + now.minute * 60 + now.second)
            #     print(f'Waiting during lunch break for {wait_time} seconds')
            #     time.sleep(wait_time)
            #     continue
            
            # Check if current time is outside trading hours (9:30 to 16:00)
            if now < dtime(9, 30) or now > dtime(16, 0):
                next_start_time = dtime(9, 30)
                if now > dtime(16, 0):
                    # Calculate time until 9:30 the next day
                    next_start_datetime = datetime.combine(datetime.now().date() + timedelta(days=1), next_start_time)
                else:
                    # Calculate time until 9:30 today
                    next_start_datetime = datetime.combine(datetime.now().date(), next_start_time)
                wait_time = (next_start_datetime - datetime.now()).total_seconds()
                print(f'Waiting until next trading day for {wait_time} seconds')
                time.sleep(wait_time)
                continue
            
            self.update()
            print(f'Waiting for next update in {self.interval} seconds')
            time.sleep(self.interval)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    scheduler = Scheduler(20)
    scheduler.start()