import pandas as pd


def create_ma_signal(df, params=None):
    """
    当短期均线上穿长期均线时做多,当长期均线下穿短期均线时平仓
    :param df: fq_收盘价
    :param params: [short,long]
    :return: 新增signal列
    """
    if params is None:
        params = [10, 90]
    short_ma = params[0]
    long_ma = params[1]
    # sort
    df['ma_long'] = df['fq_收盘价'].rolling(long_ma, min_periods=1).mean()
    df['ma_short'] = df['fq_收盘价'].rolling(short_ma, min_periods=1).mean()
    condition1 = df[(df['ma_short'] > df['ma_long']) & (df['ma_short'].shift() <= df['ma_long'].shift())].index
    condition2 = df[(df['ma_short'] < df['ma_long']) & (df['ma_short'].shift() >= df['ma_long'].shift())].index
    df.loc[condition1, 'signal'] = 1
    df.loc[condition2, 'signal'] = 0
    df.fillna(method='ffill', inplace=True)
    df.fillna(value=0, inplace=True)
    df.drop(['ma_long', 'ma_short'], axis=1, inplace=True)
    return df


def create_kdj_signal(df, N=40):
    # 计算KDJ指标
    df['low'] = df["fq_收盘价"].rolling(N).min()
    df['high'] = df["fq_收盘价"].rolling(N).max()
    df["Stochastics"] = (df["fq_收盘价"] - df["low"]) / (df["high"] - df["low"]) * 100
    df["K"] = df["Stochastics"].ewm(span=(3 - 1), adjust=False).mean()
    df["D"] = df["K"].ewm(span=(3 - 1), adjust=False).mean()
    # 计算开仓平仓条件
    condition_open = (df["D"] < 20) & (df["K"] > df["D"]) & (df['K'].shift() <= df["D"].shift())
    condition_close = (df["D"] > 80) & (df["K"] < df["D"]) & (df['K'].shift() >= df["D"].shift())
    # 产生策略信号
    df.loc[condition_open, 'signal'] = 1
    df.loc[condition_close, 'signal'] = 0
    df.fillna(method='ffill', inplace=True)
    df.fillna(value=0, inplace=True)
    df.drop(['K', 'D', 'Stochastics', "low", "high"], axis=1, inplace=True)
    return df