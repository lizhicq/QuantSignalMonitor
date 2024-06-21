import heapq

# Dictionary of product sales
product_sales = {
    'P100': 120,
    'P101': 450,
    'P102': 240,
    'P103': 320,
    'P104': 180
}

# Use nlargest to find the top 3 products with the highest sales
top_3_sales = heapq.nlargest(3, product_sales.items(), key=lambda item: item[1])

# Output the result
print(top_3_sales)
