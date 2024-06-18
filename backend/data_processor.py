def process_stock_data(stocks, intervals):
    """
    Process stock data to generate leaderboards for specified intervals.
    """
    leaderboards = {interval: [] for interval in intervals}
    for stock in stocks:
        amounts = stock.calculate_amounts(intervals)
        for interval, amount in amounts.items():
            leaderboards[interval].append({
                'stock_id': stock.stock_id,
                'name': stock.name,
                'amount': amount,
                'interval': interval
            })
    
    # Sort the leaderboards
    for interval in intervals:
        leaderboards[interval].sort(key=lambda x: x['amount'], reverse=True)
    
    return leaderboards
