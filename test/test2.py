import pandas as pd
import json

# Sample JSON data (truncated versions of arrays for brevity)
json_data = '''
{
    "state":0,"Open":14.5500,"High":15.0400,"Low":14.4600,"New":14.8400,"Volume":1622916,"Amount":2397118976,
    "LastClose":14.4800,"time":1718694000,"totalv":2123297536,"NewSZ":3030.2463,"LastCloseSZ":3015.8906,
    "NewSS":9318.4688,"LastCloseSS":9281.2529,"NewCY":1811.3649,"LastCloseCY":1806.1930,
    "BS5":[{"BuyPrice":14.8400,"BuyVolume":1194,"SellPrice":14.8500,"SellVolume":4275},
           {"BuyPrice":14.8300,"BuyVolume":7390,"SellPrice":14.8600,"SellVolume":1698}],
    "Klineresult":[{"Open":14.8400,"High":14.8400,"Low":14.8300,"Volume":12004,"Amount":17809920,"Close":14.8400,"time":1718693760},
                   {"Open":14.8400,"High":14.8400,"Low":14.8400,"Volume":1408,"Amount":2091008,"Close":14.8400,"time":1718693820}],
    "Cjmxresult":[{"New":14.8400,"BuyPrice":14.8400,"SellPrice":14.8500,"Volume":31145,"time":1718694000},
                  {"New":14.8400,"BuyPrice":14.8400,"SellPrice":14.8400,"Volume":1408,"time":1718693820}]
}
'''

# Load JSON data into a Python dictionary
data = json.loads(json_data)

# Convert parts of the JSON data into pandas DataFrames
df_bs5 = pd.DataFrame(data['BS5'])
df_klineresult = pd.DataFrame(data['Klineresult'])
df_cjmxresult = pd.DataFrame(data['Cjmxresult'])

# Print DataFrames to output
print("BS5 DataFrame:")
print(df_bs5)
print("\nKline Result DataFrame:")
print(df_klineresult)
print("\nCjmx Result DataFrame:")
print(df_cjmxresult)
