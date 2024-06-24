from backend.StockPool import StockPool
import unittest


class TestData(unittest.TestCase):
    def setUp(self) -> None:
        self.stock_pool = StockPool('data/sample/stock_mapping_sample.csv')

    def test_get_amt(self):
        self.stock_pool.update_stock_pool()
    