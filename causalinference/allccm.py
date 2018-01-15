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

    l = len(all_time_series)
    print('start to ccm... data length: ', l)
    ccm_list = [[1] * l for _ in range(l)]

    for xi, x in enumerate(all_time_series):
        yi = xi + 1
        while yi < l:
            y = all_time_series[yi]
            sc1, sc2 = calculateCCM(x, y)
            if np.isnan(sc1[0]):
                ccm_list[xi][yi] = 0
                print('nan')
            else:
                ccm_list[xi][yi] = sc1[0]
            if np.isnan(sc2[0]):
                ccm_list[xi][yi] = 0
                print('nan')
            else:
                ccm_list[yi][xi] = sc2[0]
            yi += 1

    f = open("./data/ccm_list-" + data_name + '-' + str(window_size), "w")
    json.dump(ccm_list, f)
    f.close()
    print('end ccm')
    return ccm_list


def is_sampling_point(idx, width, mean_step):
    import math
    x = idx % width
    y = math.floor(idx / width)
    if x % mean_step == 1 and y % mean_step == 0:
        return True
    return False
