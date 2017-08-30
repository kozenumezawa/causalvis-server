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
            causal_matrix = self.create_granger_matrix(body['allTimeSeries'], body['width'])
        elif method == 'CCM':
            print ('ccm')
        elif method == 'CROSS':
            causal_matrix = self.create_cross_matrix(body['allTimeSeries'], body['width'])
        else:
            causal_matrix = []


        response_msg = {
            'causalMatrix': causal_matrix
        }
        resp.body = json.dumps(response_msg)
        resp.status = falcon.HTTP_200

    @staticmethod
    def create_granger_matrix(all_time_series, width):
        all_time_series = np.array(all_time_series, dtype=np.float)
        causal_matrix = all_time_series.tolist()
        return causal_matrix

    @staticmethod
    def create_cross_matrix(all_time_series, width):
        all_time_series = np.array(all_time_series, dtype=np.float)
        causal_matrix = allcrosscorr.calc_all(all_time_series, width)
        return causal_matrix
