# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from causalinference import allcrosscorr


class CausalInference(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']
        if method == 'GRANGER':
            causal_matrix = self.create_granger_matrix(body)
        elif method == 'CCM':
            print ('ccm')
        elif method == 'CROSS':
            # causal_matrix = self.create_cross_matrix(body)
            f = open("./data/causalmatrix", "r")
            json_data = json.load(f)
            causal_matrix = json_data["causalMatrix"]
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
        width = body['width']
        max_lag = body['maxLag']
        lag_step = body['lagStep']
        mean_step = body['meanStep']
        causal_matrix = allcrosscorr.calc_all(all_time_series, width, max_lag, lag_step, mean_step)
        return causal_matrix
