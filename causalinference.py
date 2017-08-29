# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

class CausalInference(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']
        if method == 'GRANGER':
            causalMatrix = self.createGrangerMatrix(body['allTimeSeries'])
        elif method == 'CCM':
            print ('ccm')
        elif method == 'CROSS':
            causalMatrix = self.createCrossMatrix(body['allTimeSeries'])

        responseMsg = {
            'causalMatrix': causalMatrix
        }
        resp.body = json.dumps(responseMsg)
        resp.status = falcon.HTTP_200

    def createGrangerMatrix(self, allTimeSeries):
        allTimeSeries = np.array(allTimeSeries, dtype=np.float)
        causalMatrix = allTimeSeries.tolist()
        return causalMatrix

    def createCrossMatrix(self, allTimeSeries):
        allTimeSeries = np.array(allTimeSeries, dtype=np.float)
        causalMatrix = allTimeSeries.tolist()
        return causalMatrix
