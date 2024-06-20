import pandas as pd
import numpy as np
import time as time_module

# 模拟从API获取数据的函数
def fetch_data():
    new_data = {
        "Open": 943.2507,
        "High": 976.2490,
        "Low": 914.5296,
        "Volume": 2917196,
        "Amount": 12 + np.random.randint(1, 5),
        "Close": 954.1276,
        "time": int(time_module.time())  # 返回当前的epoch时间
    }
    return new_data

# 初始化DataFrame
columns = ['time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount']
df = pd.DataFrame(columns=columns)

try:
    while True:
        # 获取新数据
        new_row = pd.DataFrame([fetch_data()])  # 将新数据转换为DataFrame
        # 将新数据添加到DataFrame中
        df = pd.concat([df, new_row], ignore_index=True)
        #print(df)
        # 创建一个临时DataFrame用于计算，设置time为索引
        temp_df = df.copy()
        temp_df['time'] = temp_df['time'].apply(lambda x: pd.to_datetime(x, unit='s'))
        temp_df.set_index('time', inplace=True)

        # 计算不同时间段的成交金额总和
        rollings = {
            '1min': temp_df['Amount'].rolling('1min').sum(),
            '2min': temp_df['Amount'].rolling('2min').sum(),
            '5min': temp_df['Amount'].rolling('5min').sum(),
            '10min': temp_df['Amount'].rolling('10min').sum(),
            '20min': temp_df['Amount'].rolling('20min').sum(),
            '30min': temp_df['Amount'].rolling('30min').sum()
        }

        # 重置索引以打印
        results = pd.DataFrame(rollings).reset_index()

        # 清理数据：保留最新30分钟的数据
        # cutoff = time_module.time() - 1800
        # df = df[df['time'] >= cutoff]
        # 输出最新结果
        print(results.tail(1))  # 打印最近的数据

        # 每3秒刷新一次
        time_module.sleep(3)

except KeyboardInterrupt:
    print("Stopped by user.")
