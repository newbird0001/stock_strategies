import pandas as pd
import numpy as np


def calculate_money(df, slip_point=0.01, c_rate=2.5 / 10000, t_rate=1 / 1000):
    """
    满仓操作,收盘前5分钟操作
    :param df:
    :param slip_point:
    :param c_rate:
    :param t_rate:
    :return:
    """
    buy_condition = (df['position'] != 0) & (df['position'].shift() != df['position'])
    sell_condition = (df['position'] != 0) & (df['position'].shift(-1) != df['position'])

    df.loc[buy_condition, 'date'] = df['交易日期']
    df['date'].fillna(method='ffill', inplace=True)
    df.loc[df['position'] == 0, 'date'] = pd.NaT

    initial = 1000000

    df.loc[buy_condition, 'stock_num'] = np.floor(initial*(1 - c_rate) / ((df['前收盘价'] + slip_point) * 100)) * 100
    df.loc[buy_condition, 'cash'] = initial - df['stock_num'] * (df['前收盘价'] + slip_point) * (1 + c_rate)
    df['cash'].fillna(method='ffill', inplace=True)
    df.loc[df['position'] == 0, 'cash'] = 0
    df.loc[buy_condition, 'stock_value'] = df['stock_num'] * df['收盘价']
    t = df.groupby('date').apply(lambda x: x['fq_收盘价'] / x.iloc[0]['fq_收盘价'] * x.iloc[0]['stock_value'])
    t = t.reset_index(level=[0])
    try:
        df['stock_value'] = t['fq_收盘价']
    except Exception as e:
        print(e)
        print(t.T)
        df['stock_value'] = t.T[0]


    df['stock_num'] = df['stock_value'] / df['收盘价']

    df.loc[sell_condition, 'cash'] += df.loc[sell_condition, 'stock_num'] * (df['收盘价'] - slip_point) * (
                1 - c_rate - t_rate)
    df.loc[sell_condition, 'stock_num'] = 0
    df.loc[sell_condition, 'stock_value'] = 0

    df['net_v'] = df['stock_value'] + df['cash']
    df['wave'] = df['net_v'].pct_change(fill_method=None)
    df.loc[buy_condition, 'wave'] = df['net_v'] / initial - 1.0
    df['wave'].fillna(value=0, inplace=True)
    # df.dropna(subset=["date"], inplace=True)
    df['收益曲线'] = (1+df['wave']).cumprod()
    df["基准涨跌幅"] = df['收盘价'] / df['前收盘价'] -1.0
    df['基准收益'] = (df['收盘价'] / df['前收盘价']).cumprod()

    return df
