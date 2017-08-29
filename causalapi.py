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
            causalMatrix = self.create_granger_matrix(body['allTimeSeries'])
        elif method == 'CCM':
            print ('ccm')
        elif method == 'CROSS':
            causalMatrix = self.create_cross_matrix(body['allTimeSeries'])

        responseMsg = {
            'causalMatrix': causalMatrix
        }
        resp.body = json.dumps(responseMsg)
        resp.status = falcon.HTTP_200

    def create_granger_matrix(self, allTimeSeries):
        allTimeSeries = np.array(allTimeSeries, dtype=np.float)
        causalMatrix = allTimeSeries.tolist()
        return causalMatrix

    def create_cross_matrix(self, allTimeSeries):
        allTimeSeries = np.array(allTimeSeries, dtype=np.float)
        test = allcrosscorr.calc_all(allTimeSeries)
        causalMatrix = test.tolist()
        return causalMatrix
