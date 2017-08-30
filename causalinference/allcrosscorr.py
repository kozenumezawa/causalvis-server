# calculate causal direction using cross correlation from each point to every point
def calc_all(allTimeSeries, width):
    import numpy as np
    import math
    corrList = []
    lag = 10
    meanStep = 3

    for (i, x) in enumerate(allTimeSeries):
        if (sum(x) == 0 or (i % width) % meanStep != 1 or math.floor(i / width) % meanStep != 0):
            corrList.append([])
            continue

        corrList.append([0 for _ in range(len(allTimeSeries / meanStep / meanStep))])

        back_x = x[lag:]
        front_x = x[:len(x)-lag]
        for (j, y) in enumerate(allTimeSeries):
            if (sum(y) == 0  or (j % width) % meanStep != 1 or math.floor(j / width) % meanStep != 0):
                corrList[i][j] = 0
                continue

            corr = np.corrcoef(x, y)[0][1]
            if math.isnan(corr):
                corrList[i][j] = 0
                continue

            back_corr = np.corrcoef(back_x, y[:len(y)-lag])[0][1]
            frontCorr = np.corrcoef(front_x, y[lag:])[0][1]

            each_corr = [back_corr, corr, frontCorr]
            max_idx = each_corr.index(max(each_corr))

            if max_idx == 0:
                corrList[i][j] = 0
            elif max_idx == 1:
                corrList[i][j] = 0
            else:
                corrList[i][j] = frontCorr
    return corrList
