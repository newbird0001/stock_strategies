import time

import pandas as pd
from stock_strategy.select_time.Evaluate import calculate_money
from stock_strategy.select_time.Signal import create_kdj_signal
from stock_strategy.General_Funtion import calculate_limit, calculate_fq_price
from stock_strategy.select_time.Position import creat_position_at_close
pd.set_option('display.max_rows', 5000)
# 读入数据
df = pd.read_csv(
    filepath_or_buffer='C:\\Users\\TTT\\Desktop\\pythonProject\\data\\home_work_data\\stock\\sz000002.csv',
    encoding='gbk',
    skiprows=1,
    parse_dates=['交易日期'],
    on_bad_lines='skip',
    na_values='NULL'
)
# 处理数据
df.drop_duplicates('交易日期', inplace=True)
# 计算涨停价和复权价
df = calculate_limit(df)
df = calculate_fq_price(df)
# 产生策略参数列表
params = range(9, 40 + 1)
# 新建表格用于存储数据
dfr = pd.DataFrame()
# 遍历参数列表生成策略结果
for param in params:
    # 产生信号和持仓
    df1 = create_kdj_signal(df.copy(), param)
    df1 = creat_position_at_close(df1)
    # 股权分置改革后的数据
    df1 = df1.iloc[250 - 1:]
    df1 = df1[df1['交易日期'] >= pd.to_datetime('2007-01-01')]
    df1.sort_values('交易日期', inplace=True)
    df1.reset_index(drop=True, inplace=True)
    df1 = calculate_money(df1)
    print("N=:", param, "策略收益为:", df1.iloc[-1]['收益曲线'], "基准收益为:", df1.iloc[-1]['基准收益'])
    dfr.loc["N=:" + str(param), "策略收益"] = df1.iloc[-1]['收益曲线']
    dfr.loc["N=:" + str(param), "基准收益"] = df1.iloc[-1]['基准收益']
dfr.sort_values(by=['策略收益'], ascending=0, inplace=True)
print(dfr)

