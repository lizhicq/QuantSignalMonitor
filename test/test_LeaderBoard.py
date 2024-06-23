import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from backend.Stock import Stock
from backend.StockPool import StockPool
from config.data_config import *
class TestStockPool(unittest.TestCase):
    def setUp(self):
        # Mock the CSV reading to set up the stock pool
        stock_data = {
            'StockId': [f'{i:03}' for i in range(1, 51)],
            'StockName': [f'Stock{i:03}' for i in range(1, 51)],
            'WindCode': [f'W{i:05}' for i in range(1, 51)]
        }
        mock_df = pd.DataFrame(stock_data)
        mock_df.set_index('StockId', inplace=True)

        # Patching pandas read_csv to return a mock dataframe
        patcher = patch('pandas.read_csv', return_value=mock_df)
        self.addCleanup(patcher.stop)
        self.mock_read_csv = patcher.start()

        # Initializing the StockPool which will use the mocked read_csv
        self.stock_pool = StockPool()

    @patch('backend.StockPool.fetch_single_stock_id')
    @patch('backend.StockPool.fetch_multi_stock_id')
    def test_create_leaderboard(self, mock_fetch_multi, mock_fetch_single):
        # Setup mock data for multi_stock_id and single_stock_id
        mock_fetch_multi.return_value = {'pk': [{'StockId': f'{i:03}', 'data': 'some_data'} for i in range(1, 51)]}
        mock_fetch_single.side_effect = lambda stock_id: {
            'Klineresult': [
                {'Open': i, 'High': i*1.05, 'Low': i*0.95, 'Close': i*1.02, 'Amount': i*1000, 'time': 1718953200+i}
                for i in range(100, 150)
            ]
        }

        # Call the method under test
        top_num = 10
        self.stock_pool.create_leaderboard(top_num)

        # Check if the leaderboard has been populated for each window
        for window in {1, 2, 3, 5, 10, 20, 30}:
            self.assertIn(window, self.stock_pool.leaderboard)
            self.assertEqual(len(self.stock_pool.leaderboard[window]), 10)
            # Check specific metrics for the first stock
            first_stock = self.stock_pool.leaderboard[window][0]
            self.assertGreater(first_stock['TotalAmount'], 0)
            self.assertNotEqual(first_stock['PriceIncrease'], 0)
            self.assertNotEqual(first_stock['IntervalPriceIncrease'], 0)
            self.assertGreaterEqual(first_stock['StatisticalInterval'], 0)
            self.assertGreater(first_stock['PriceSurge'], 0)

            print(f"Window {window}:")
            for stock in self.stock_pool.leaderboard[window]:
                print(stock)

if __name__ == '__main__':
    unittest.main()
