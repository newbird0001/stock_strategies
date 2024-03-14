def creat_position_at_close(df):
    """
    计算持仓,并考虑涨停无法买和跌停无法卖的情况
    :param df:
    :return:
    """
    df['position'] = df['signal'].shift()
    up_stop = df['收盘价'] >= df['涨停价']
    df.loc[(up_stop.shift()) & (df['signal'].shift() == 1), 'position'] = None
    down_stop = df['收盘价'] <= df['跌停价']
    df.loc[(down_stop.shift()) & (df['signal'].shift() == 0), 'position'] = None
    df.fillna(method='ffill', inplace=True)
    df.fillna(value=0, inplace=True)
    return df