from backend.StockPool import StockPool
from backend.Stock import Stock
from unittest.mock import patch, MagicMock
from config.data_config import DATA_PATH_CONFIG
import unittest,json
import pandas as pd


# Expanded Klineresult for mocking in the test
kline_result_expanded = [
    {'Open': 33.0, 'High': 33.2, 'Low': 32.36, 'Close': 32.7, 'Volume': 85801, 'Amount': 280375168, 'time': 1718953200},
    {'Open': 32.7, 'High': 33.5, 'Low': 32.5, 'Close': 33.2, 'Volume': 60000, 'Amount': 198000000, 'time': 1718953260},
    {'Open': 33.2, 'High': 33.6, 'Low': 33.1, 'Close': 33.5, 'Volume': 65000, 'Amount': 216450000, 'time': 1718953320},
    {'Open': 33.5, 'High': 34.0, 'Low': 33.4, 'Close': 33.9, 'Volume': 70000, 'Amount': 237300000, 'time': 1718953380},
    {'Open': 33.9, 'High': 34.3, 'Low': 33.8, 'Close': 34.1, 'Volume': 50000, 'Amount': 170500000, 'time': 1718953440},
    {'Open': 34.1, 'High': 34.6, 'Low': 34.0, 'Close': 34.5, 'Volume': 55000, 'Amount': 189750000, 'time': 1718953500},
    {'Open': 34.5, 'High': 34.7, 'Low': 34.2, 'Close': 34.4, 'Volume': 53000, 'Amount': 182420000, 'time': 1718953560},
    {'Open': 34.4, 'High': 34.8, 'Low': 34.3, 'Close': 34.6, 'Volume': 60000, 'Amount': 207600000, 'time': 1718953620},
    {'Open': 34.6, 'High': 35.0, 'Low': 34.5, 'Close': 34.9, 'Volume': 61000, 'Amount': 212990000, 'time': 1718953680},
    {'Open': 34.9, 'High': 35.3, 'Low': 34.8, 'Close': 35.1, 'Volume': 62000, 'Amount': 217620000, 'time': 1718953740},
    {'Open': 35.1, 'High': 35.5, 'Low': 35.0, 'Close': 35.3, 'Volume': 58000, 'Amount': 204740000, 'time': 1718953800},
    {'Open': 35.3, 'High': 35.7, 'Low': 35.2, 'Close': 35.5, 'Volume': 57000, 'Amount': 202350000, 'time': 1718953860},
    {'Open': 35.5, 'High': 35.9, 'Low': 35.4, 'Close': 35.7, 'Volume': 56000, 'Amount': 199920000, 'time': 1718953920},
    {'Open': 35.7, 'High': 36.1, 'Low': 35.6, 'Close': 35.9, 'Volume': 59000, 'Amount': 211890000, 'time': 1718953980},
    {'Open': 35.9, 'High': 36.3, 'Low': 35.8, 'Close': 36.1, 'Volume': 60000, 'Amount': 216600000, 'time': 1718954040},
    {'Open': 36.1, 'High': 36.5, 'Low': 36.0, 'Close': 36.3, 'Volume': 62000, 'Amount': 225060000, 'time': 1718954100},
    {'Open': 36.3, 'High': 36.7, 'Low': 36.2, 'Close': 36.5, 'Volume': 63000, 'Amount': 229950000, 'time': 1718954160},
    {'Open': 36.5, 'High': 36.9, 'Low': 36.4, 'Close': 36.7, 'Volume': 64000, 'Amount': 234880000, 'time': 1718954220},
    {'Open': 36.7, 'High': 37.1, 'Low': 36.6, 'Close': 36.9, 'Volume': 65000, 'Amount': 239850000, 'time': 1718954280},
    {'Open': 36.9, 'High': 37.3, 'Low': 36.8, 'Close': 37.1, 'Volume': 66000, 'Amount': 244860000, 'time': 1718954340}
]
with open(DATA_PATH_CONFIG['fetch_single_stock_sample'], 'rb') as f:
    FETCH_SINGLE_STOCK_SAMPLE_DATA = json.load(f) 
    
with open(DATA_PATH_CONFIG['fetch_multi_stock_sample'], 'rb') as f:
    FETCH_MULTI_STOCK_SAMPLE_DATA = json.load(f) 

class TestStockPool(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_constructor(self, mock_read_csv):
        # Setup mock DataFrame for pandas.read_csv
        mock_data = pd.DataFrame({
            'StockId': [101, 102],
            'StockName': ['Alpha', 'Beta'],
            'WindCode': ['A101', 'B102']
        }).set_index('StockId')
        mock_read_csv.return_value = mock_data

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
        mock_fetch_multi_stock_id.return_value = {'pk': [{'StokId': 101, 'Amount': 300}, {'StokId': 102, 'Amount': 450}]}

        # Run update_stock_pool
        stock_pool.update_stock_pool()

        # Assert add_minute_data was called with correct records
        stock_pool.total_pool[101].add_minute_data.assert_called_once_with({'StokId': 101, 'Amount': 300})
        stock_pool.total_pool[102].add_minute_data.assert_called_once_with({'StokId': 102, 'Amount': 450})
    
    
    @patch('backend.StockPool.Stock')
    @patch('pandas.read_csv')
    def test_get_top_n_stocks_within_w_min(self, mock_read_csv, mock_Stock):
        # Setup DataFrame for read_csv
        mock_read_csv.return_value = pd.DataFrame({
            'StokId': range(1, 31),  # Create 30 stock items
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

        # Test get_top_n_stocks_within_w_min
        top_stocks = stock_pool.get_top_amt_stocks(30, 20)
        self.assertEqual(len(top_stocks), 20)  # Check if exactly 20 items are returned
        self.assertTrue(all(top_stocks[i][1].get_amt_of_last_n_minutes(30) >= top_stocks[i + 1][1].get_amt_of_last_n_minutes(30) 
                            for i in range(19)), "Stocks should be sorted by amount")

        
# To run the test
if __name__ == '__main__':
    unittest.main()
