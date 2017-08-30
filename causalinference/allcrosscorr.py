# calculate causal direction using cross correlation from each point to every point
def calc_all(all_time_series, max_lag, lag_step):
    import numpy as np
    import math
    import json

    corr_list = []

    for (row_idx, x) in enumerate(all_time_series):
        corr_list.append([0 for _ in range(len(all_time_series))])

        for (col_idx, y) in enumerate(all_time_series):
            zero_lag_corr = np.corrcoef(x, y)[0][1]
            if math.isnan(zero_lag_corr):
                corr_list[row_idx][col_idx] = 0
                continue

            plus_lag_corr = []
            minus_lag_corr = []
            for lag in range(lag_step, max_lag, lag_step):
                # if corr(x, y[lag:]) > corr(x, y) : there is causality from x to y
                plus_lag_corr.append(np.corrcoef(x[:len(x) - lag], y[lag:])[0][1])
                minus_lag_corr.append(np.corrcoef(x[lag:], y[:len(y) - lag])[0][1])

            each_corr = [max(minus_lag_corr), zero_lag_corr, max(plus_lag_corr)]
            max_idx = each_corr.index(max(each_corr))

            if max_idx == 0:
                corr_list[row_idx][col_idx] = 0
            elif max_idx == 1:
                corr_list[row_idx][col_idx] = 0
            else:
                corr_list[row_idx][col_idx] = max(each_corr)

    saveJSON = {
        'causalMatrix': corr_list
    }
    f = open("./data/causalmatrix", "w")
    json.dump(saveJSON, f)
    f.close()

    return corr_list

def is_sampling_point(idx, width, mean_step):
    import math
    x = idx % width
    y = math.floor(idx / width)
    if x % mean_step == 1 and y % mean_step == 0:
        return True
    return False
