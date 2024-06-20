from data.stock_info_sample import sample
import pandas as pd 


df = pd.DataFrame(sample['Klineresult'])
windows = [1, 2, 3, 5, 10, 20]

results = {}

for window in windows:
    # 滚动窗口
    df_roll = df.rolling(window=window, on='time')
    
    # 成交金额（Total Amount） - 10分钟内所有交易的成交金额总和。
    # 涨幅（Price Increase） - 10分钟结束时的收盘价与开始时的开盘价之差。
    # 区间涨幅（Interval Price Increase） - 10分钟内最高价与最低价之差。
    # 统计区间（Statistical Interval） - 选择的10分钟内数据点的时间范围。
    # 拉升幅度（Price Surge） - 最低价到最高价的涨幅比例。
    # 计算各项指标
    total_amount = df_roll['Amount'].sum()
    price_increase = df_roll['Close'].apply(lambda x: x.iloc[-1]) - df_roll['Open'].apply(lambda x: x.iloc[0])
    statistical_interval = df_roll['time'].apply(lambda x: x.max() - x.min())
    
    range_high, range_low = df_roll['High'].max(), df_roll['Low'].min()
    interval_price_increase = range_high - range_low
    price_surge = (range_high - range_low) /range_low

    # 存储结果
    results[window] = {
        'Total Amount': total_amount,
        'Price Increase': price_increase,
        'Interval Price Increase': interval_price_increase,
        'Statistical Interval': statistical_interval,
        'Price Surge': price_surge
    }

# 展示结果，例如10分钟窗口
print(results[10])