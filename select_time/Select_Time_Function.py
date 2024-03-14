def create_params_in_ma(short=range(10, 100, 10), long=range(10, 200, 10)):
    """
    简单产生一系列合法的短期值和长期值
    :param short:
    :param long:
    :return:
    """
    params_list = []
    for short_p in short:
        for long_p in long:
            if short_p >= long_p:
                continue
            else:
                params_list.append([short_p, long_p])
    return params_list
