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
        mock_read_csv.return_value = mock_data

        # Importing the StockPool class
        from backend.StockPool import StockPool

        # Create an instance of StockPool
        stock_pool = StockPool()

        # Assert that total_pool is correctly populated
        self.assertEqual(len(stock_pool.total_pool), 2)
        self.assertIn(101, stock_pool.total_pool)
        self.assertIn(102, stock_pool.total_pool)
        self.assertEqual(stock_pool.total_pool[101].name, 'Alpha')

    @patch('backend.StockPool.fetch_multi_stock_id')
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
    
    
    @patch('backend.StockPool.Stock')
    @patch('pandas.read_csv')
    def test_get_top_amt_stocks(self, mock_read_csv, mock_Stock):
        # Setup DataFrame for read_csv
        mock_read_csv.return_value = pd.DataFrame({
            'StockId': range(1, 31),  # Create 30 stock items
            'StockName': [f'Stock{i}' for i in range(1, 31)],
            'WindCode': [f'WND{i}' for i in range(1, 31)]
        })

        # Setup Stock instances
        mock_stock_instance = MagicMock()
        mock_Stock.return_value = mock_stock_instance

        # Mock get_amt_of_last_n_minutes to return different values
        mock_stock_instance.get_amt_of_last_n_minutes.side_effect = lambda interval: interval + 100

        # Initialize StockPool
        stock_pool = StockPool()

        # Assuming stock pool creates its own stock instances from the DataFrame
        # Populate the pool with mocked stock instances
        for i in range(1, 31):
            stock_pool.total_pool[i] = mock_stock_instance

        # Test get_top_amt_stocks
        top_stocks = stock_pool.get_top_amt_stocks(30, 20)
        self.assertEqual(len(top_stocks), 20)  # Check if exactly 20 items are returned
        self.assertTrue(all(top_stocks[i][1].get_amt_of_last_n_minutes(30) >= top_stocks[i + 1][1].get_amt_of_last_n_minutes(30) 
                            for i in range(19)), "Stocks should be sorted by amount")

# To run the test
if __name__ == '__main__':
    unittest.main()
