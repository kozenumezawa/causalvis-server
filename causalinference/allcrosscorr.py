# calculate causal direction using cross correlation from each point to every point
def calc_all(all_time_series, width):
    import numpy as np
    import math

    corr_list = []
    max_lag = 20
    lag_step = 2
    mean_step = 3

    for (i, x) in enumerate(all_time_series):
        if (sum(x) == 0 or (i % width) % mean_step != 1 or math.floor(i / width) % mean_step != 0):
            corr_list.append([])
            continue
        corr_list.append([0 for _ in range(len(all_time_series))])

        for (j, y) in enumerate(all_time_series):
            if (sum(y) == 0  or (j % width) % mean_step != 1 or math.floor(j / width) % mean_step != 0):
                corr_list[i][j] = 0
                continue

            zero_lag_corr = np.corrcoef(x, y)[0][1]
            if math.isnan(zero_lag_corr):
                corr_list[i][j] = 0
                continue

            plus_lag_corr = []
            minus_lag_corr = []
            for lag in range(lag_step, max_lag, lag_step):
                # if corr(x, y) > corr(x, y[lag:]): there is causality from x to y
                plus_lag_corr.append(np.corrcoef(x[:len(x) - lag], y[lag:])[0][1])
                minus_lag_corr.append(np.corrcoef(x[lag:], y[:len(y) - lag])[0][1])

            each_corr = [max(minus_lag_corr), zero_lag_corr, max(plus_lag_corr)]
            max_idx = each_corr.index(max(each_corr))

            if max_idx == 0:
                corr_list[i][j] = 0
            elif max_idx == 1:
                corr_list[i][j] = 0
            else:
                corr_list[i][j] = max(each_corr)
    return corr_list
