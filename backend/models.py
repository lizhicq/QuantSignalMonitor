class Stock:
    def __init__(self, stock_id, name):
        self.stock_id = stock_id
        self.name = name
        self.transactions = []  # List of transactions to compute various intervals

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def calculate_amounts(self, intervals):
        """
        Calculate the total transaction amounts for the specified intervals.
        """
        amounts = {}
        current_time = max(transaction['time'] for transaction in self.transactions)
        for interval in intervals:
            start_time = current_time - interval
            amounts[interval] = sum(transaction['amount'] for transaction in self.transactions if transaction['time'] >= start_time)
        return amounts
