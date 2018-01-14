def calc_all_ccm(all_time_series, max_lag, lag_step, data_name, window_size):
    import numpy as np
    import json
    import skccm as ccm
    from skccm.utilities import train_test_split

    def calculateCCM(x, y):
        lag = 1
        embed = 2
        lib_lens = [len(x)]
        e1 = ccm.Embed(np.array(x))
        e2 = ccm.Embed(np.array(y))
        X1 = e1.embed_vectors_1d(lag, embed)
        X2 = e2.embed_vectors_1d(lag, embed)
        x1tr, x1te, x2tr, x2te = train_test_split(X1, X2, percent=.75)
        c = ccm.CCM()
        c.fit(x1tr, x2tr)
        x1p, x2p = c.predict(x1te, x2te, lib_lengths=lib_lens)
        sc1, sc2 = c.score()
        return sc1, sc2

    ccm_list = []
    lag_list = []

    for (row_idx, x) in enumerate(all_time_series):
        print(row_idx)
        row_ccm = []
        row_lag = []

        for y in all_time_series:
            zero_lag_ccm = calculateCCM(x, y)[0]

            plus_lag_ccm = []
            minus_lag_ccm = []
            for lag in range(lag_step, max_lag, lag_step):
                # if corr(x, y[lag:]) > corr(x, y) : there is causality from x
                # to y
                plus_lag_ccm.append(
                    calculateCCM(x[:len(x) - lag], y[lag:])[0])
                minus_lag_ccm.append(
                    calculateCCM(x[lag:], y[:len(y) - lag])[0])

            each_ccm = [max(minus_lag_ccm), zero_lag_ccm,
                        max(plus_lag_ccm)]
            max_idx = each_ccm.index(max(each_ccm))

            if max_idx == 0:
                # when y -> x
                row_ccm.append(0)
                row_lag.append(0)
            elif max_idx == 1:
                row_ccm.append(0)
                row_lag.append(0)
            else:
                # when x -> y
                row_ccm.append(max(each_ccm))
                row_lag.append(plus_lag_ccm.index(max(plus_lag_ccm)) + 1)
        ccm_list.append(row_ccm)
        lag_list.append(row_lag)

    f = open("./data/ccm_list-" + data_name + '-' + str(window_size), "w")
    json.dump(ccm_list, f)
    f.close()

    f = open("./data/lag_list-" + data_name + '-' + str(window_size), "w")
    json.dump(lag_list, f)
    f.close()
    return (ccm_list, lag_list)


def is_sampling_point(idx, width, mean_step):
    import math
    x = idx % width
    y = math.floor(idx / width)
    if x % mean_step == 1 and y % mean_step == 0:
        return True
    return False
