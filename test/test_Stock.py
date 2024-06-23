import unittest
from collections import deque
from backend.Stock import *
from backend.data_fetcher import *

class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock(stock_id=123, name="TestStock", wind_code="TST123")
        self.stock.minute_data = deque([{'Amount': 100}, {'Amount': 153}, {'Amount': 201}], maxlen=31)
        self.stock.minute_amt = deque([100, 153, 201], maxlen=31)

    def test_add_minute_data_no_duplicate(self):
        record = {'Amount': 250}
        self.stock.add_minute_data(record)
        self.assertEqual(len(self.stock.minute_data), 4)
        self.assertEqual(self.stock.minute_amt[-1], 250)

    def test_add_minute_data_with_duplicate(self):
        record = {'Amount': 201}
        self.stock.add_minute_data(record)
        self.assertEqual(len(self.stock.minute_data), 3)  # No new record should be added

    def test_get_amt_of_last_n_minutes(self):
        # Add another amount to enable proper testing
        self.stock.add_minute_data({'Amount': 252})
        result = self.stock.get_amt_of_last_n_minutes(2)
        self.assertEqual(result, 99)  # 252 - 153
    
        
# To run the test
if __name__ == '__main__':
    unittest.main()
