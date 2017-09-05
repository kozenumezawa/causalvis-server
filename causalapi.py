# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from causalinference import allcrosscorr


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
            if data_name == 'real' or data_name == 'sim':
                f = open("./data/causalmatrix-" + data_name, "r")
                json_data = json.load(f)
                causal_matrix = json_data["causalMatrix"]

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

        causal_matrix = allcrosscorr.calc_all(all_time_series,  max_lag, lag_step, data_name)
        return causal_matrix
