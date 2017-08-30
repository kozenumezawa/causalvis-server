# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from causalinference import allcrosscorr


class Clustering(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']

        if method == 'IRM':
            cluster_matrix = self.infinite_relational_modeling(body)
        else:
            cluster_matrix = []

        response_msg = {
            'clusterMatrix': cluster_matrix
        }
        resp.body = json.dumps(response_msg)
        resp.status = falcon.HTTP_200

    @staticmethod
    def infinite_relational_modeling(body):
        causal_matrix = np.array(body['causalMatrix'], dtype=np.float)
        return causal_matrix.tolist()
