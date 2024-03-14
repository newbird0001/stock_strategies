from decimal import Decimal, ROUND_HALF_UP

import pandas as pd


def calculate_limit(df):
    """
    计算股票的涨跌停价
    :param df: 包含前收盘价,股票名称,股票代码，开盘价,最高价,最低价
    :return: 新增涨停价,跌停价,一字涨停,一字跌停,开盘涨停,开盘跌停六列
    """
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    problem_stock = df['股票名称'].str.contains('ST')
    df['涨停价'] = df['前收盘价'] * 1.1
    df['跌停价'] = df['前收盘价'] * 0.9
    df.loc[problem_stock, '涨停价'] = df['前收盘价'] * 1.05
    df.loc[problem_stock, '跌停价'] = df['前收盘价'] * 1.05

    kc_stock = df['股票代码'].str.startswith('sh68')
    cy_stock = df['股票代码'].str.startswith('sz30')

    df.loc[(kc_stock | cy_stock) & (df['交易日期'] >= pd.to_datetime('2020-08-04')), '涨停价'] = df['前收盘价'] * 1.2
    df.loc[(kc_stock | cy_stock) & (df['交易日期'] >= pd.to_datetime('2020-08-04')), '跌停价'] = df['前收盘价'] * 0.8

    bj_name = df['股票名称'].str.startswith('bj')
    df.loc[bj_name, '涨停价'] = df['前收盘价'] * 1.3
    df.loc[bj_name, '跌停价'] = df['前收盘价'] * 0.7

    df['涨停价'] = df['涨停价'].apply(lambda x: float(Decimal(x * 100).quantize(Decimal('1'), ROUND_HALF_UP)) / 100)
    df['跌停价'] = df['跌停价'].apply(lambda x: float(Decimal(x * 100).quantize(Decimal('1'), ROUND_HALF_UP)) / 100)

    # 若需要一字涨停等情况的判断,请在本行下方实现
    df.loc[df['最低价'] >= df['涨停价'], '一字涨停'] = 1
    df.loc[df['最高价'] <= df['跌停价'], '一字跌停'] = 1
    df.loc[df['开盘价'] >= df['涨停价'], '开盘涨停'] = 1
    df.loc[df['开盘价'] <= df['跌停价'], '开盘跌停'] = 1
    df['一字涨停'].fillna(value=0, inplace=True)
    df['一字跌停'].fillna(value=0, inplace=True)
    df['开盘涨停'].fillna(value=0, inplace=True)
    df['开盘跌停'].fillna(value=0, inplace=True)
    return df


def calculate_fq_price(df, fq_type="后复权"):
    """
    用于计算股票的复权价
    :param df: 需要包含:开盘价,最高价,最低价,收盘价,前收盘价
    :param fq_type: 前复权或后复权
    :return: 新增四列:fq_开盘价,fq_最高价,fq_最低价,fq_收盘价
    """
    df['复权因子'] = (df['收盘价'] / df['前收盘价']).cumprod()
    if fq_type == "前复权":
        df['fq_收盘价'] = df['复权因子'] * (df.iloc[-1]['收盘价'] / df.iloc[-1]['复权因子'])
    elif fq_type == "后复权":
        df['fq_收盘价'] = df['复权因子'] * (df.iloc[0]['收盘价'] / df.iloc[0]['复权因子'])
    else:
        print("错误的复权类型%s" % fq_type)

    df['fq_开盘价'] = df['开盘价'] / df['收盘价'] * df['fq_收盘价']
    df['fq_最高价'] = df['最高价'] / df['收盘价'] * df['fq_收盘价']
    df['fq_最低价'] = df['最低价'] / df['收盘价'] * df['fq_收盘价']

    df.drop(['复权因子'], axis=1, inplace=True)

    return df



