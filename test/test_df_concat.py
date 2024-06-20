import pandas as pd
import numpy as np

# Assuming df is the existing DataFrame
# Initialize an empty DataFrame with the correct column order
df = pd.DataFrame(columns=['time', 'Open', 'High', 'Low', 'Volume', 'Amount', 'Close'])

# Simulating the existing data
df = pd.concat([
    df,
    pd.DataFrame([{
        "time": pd.Timestamp.now(),  # Current time, adjusted to demonstrate
        "Open": 943.2507,
        "High": 976.2490,
        "Low": 914.5296,
        "Volume": 2917196,
        "Amount": 1456,  # Random example amount
        "Close": 954.1276,
    }])
], ignore_index=True)

# Print to check the data before adding new data
print("Before adding new data:\n", df)

# New data to append
new_data = {
    "time": pd.Timestamp.now(),  # Current time
    "Open": 943.2507,
    "High": 976.2490,
    "Low": 914.5296,
    "Volume": 2917196,
    "Amount": 1234 + np.random.randint(100, 1000),  # Random amount variation
    "Close": 954.1276,
}


# Create a DataFrame from new_data ensuring the column order
new_row_df = pd.DataFrame([new_data], columns=df.columns)

# Concatenate the new row DataFrame to the original DataFrame
df = pd.concat([df, new_row_df], ignore_index=True)

# Print the updated DataFrame
print("After adding new data:\n", df)
