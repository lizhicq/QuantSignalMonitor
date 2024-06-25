from backend.StockPool import StockPool
import unittest


class TestData(unittest.TestCase):
    def setUp(self) -> None:
        self.stock_pool = StockPool()
        
    def test(self):
        self.stock_pool.update_stock_pool()
    

if __name__ == "__main__":
    unittest.main()