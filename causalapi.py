# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from causalinference import allcrosscorr
from constants import DATA_SIM
from constants import DATA_WILD
from constants import DATA_TRP3
from constants import DATA_TRP3_RAW

class CausalInference(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']
        data_name = body['dataName']

        if method == 'GRANGER':
            causal_matrix = self.create_granger_matrix(body)
        elif method == 'CCM':
            print ('ccm')
        elif method == 'CROSS':
            window_size = body["windowSize"]
            if data_name == DATA_TRP3:
                if window_size == 3 or window_size == 5 or window_size == 7:
                    f = open("./data/causalmatrix-" + data_name + '-' + str(window_size), "r")
                    json_data = json.load(f)
                    causal_matrix = json_data["causalMatrix"]
                else:
                    causal_matrix = self.create_cross_matrix(body)
            elif data_name == DATA_SIM:
                f = open("./data/causalmatrix-sim", "r")
                json_data = json.load(f)
                causal_matrix = json_data["causalMatrix"]
            elif data_name == DATA_WILD:
                f = open("./data/causalmatrix-data_wild", "r")
                json_data = json.load(f)
                causal_matrix = json_data["causalMatrix"]
            elif data_name == DATA_TRP3_RAW:
                f = open("./data/causalmatrix-data_trp3_raw", "r")
                json_data = json.load(f)
                causal_matrix = json_data["causalMatrix"]
                # causal_matrix = self.create_cross_matrix(body)
            else:
                # causal_matrix = self.create_cross_matrix(body)
                causal_matrix = []
        else:
            causal_matrix = []


        response_msg = {
            'causalMatrix': causal_matrix
        }
        resp.body = json.dumps(response_msg)
        resp.status = falcon.HTTP_200

    @staticmethod
    def create_granger_matrix(body):
        all_time_series = np.array(body['allTimeSeries'], dtype=np.float)
        causal_matrix = all_time_series.tolist()
        return causal_matrix

    @staticmethod
    def create_cross_matrix(body):
        all_time_series = np.array(body['allTimeSeries'], dtype=np.float)
        max_lag = body['maxLag']
        lag_step = body['lagStep']
        data_name = body['dataName']
        window_size = body['windowSize']

        causal_matrix = allcrosscorr.calc_all(all_time_series,  max_lag, lag_step, data_name, window_size)
        return causal_matrix
