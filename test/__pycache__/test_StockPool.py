from backend.StockPool import StockPool
from unittest.mock import patch, MagicMock
import unittest
import pandas as pd

class TestStockPool(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_constructor(self, mock_read_csv):
        # Setup mock DataFrame for pandas.read_csv
        mock_data = pd.DataFrame({
            'StockId': [101, 102],
            'StockName': ['Alpha', 'Beta'],
            'WindCode': ['A101', 'B102']
        })
        mock_read_csv.return_value = mock_data.iterrows()

        # Importing the StockPool class
        from backend.StockPool import StockPool

        # Create an instance of StockPool
        stock_pool = StockPool()

        # Assert that total_pool is correctly populated
        self.assertEqual(len(stock_pool.total_pool), 2)
        self.assertIn(101, stock_pool.total_pool)
        self.assertIn(102, stock_pool.total_pool)
        self.assertEqual(stock_pool.total_pool[101].name, 'Alpha')

    @patch('backend.data_fetcher.fetch_multi_stock_id')
    @patch('backend.Stock.Stock.add_minute_data')
    def test_update_stock_pool(self, mock_add_minute_data, mock_fetch_multi_stock_id):
        # Setup the StockPool with mocked constructor to avoid file reading
        from backend.StockPool import StockPool
        stock_pool = StockPool.__new__(StockPool)
        stock_pool.total_pool = {
            101: MagicMock(),
            102: MagicMock()
        }

        # Mock data returned from fetch_multi_stock_id
        mock_fetch_multi_stock_id.return_value = {'pk': [{'StockId': 101, 'Amount': 300}, {'StockId': 102, 'Amount': 450}]}

        # Run update_stock_pool
        stock_pool.update_stock_pool()

        # Assert add_minute_data was called with correct records
        stock_pool.total_pool[101].add_minute_data.assert_called_once_with({'StockId': 101, 'Amount': 300})
        stock_pool.total_pool[102].add_minute_data.assert_called_once_with({'StockId': 102, 'Amount': 450})

# To run the test
if __name__ == '__main__':
    unittest.main()
