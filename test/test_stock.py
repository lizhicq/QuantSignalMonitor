from backend.models import Stock
import unittest

class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock(stock_id="12345", name="TestStock")
        self.transactions = [
            {'time': 1590, 'amount': 500, 'price': 10},
            {'time': 1600, 'amount': 300, 'price': 15},
            {'time': 1610, 'amount': 200, 'price': 20}
        ]
        for t in self.transactions:
            self.stock.add_transaction(t)

    def test_calculate_amounts(self):
        intervals = [10, 20]
        results = self.stock.calculate_amounts(intervals)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[10]['amount'], 500 + 300)
        self.assertAlmostEqual(results[10]['price_gain'], 50.0)  # from 10 to 15

        self.assertEqual(results[20]['amount'], 500 + 300 + 200)
        self.assertAlmostEqual(results[20]['price_gain'], 100.0)  # from 10 to 20

if __name__ == '__main__':
    unittest.main()