# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from clustering import irm


class Clustering(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']

        if method == 'IRM':
            cluster_matrix = self.infinite_relational_model(body)
        else:
            cluster_matrix = []

        response_msg = {
            'clusterMatrix': cluster_matrix
        }
        resp.body = json.dumps(response_msg)
        resp.status = falcon.HTTP_200

    @staticmethod
    def infinite_relational_model(body):
        causal_matrix = np.array(body['causalMatrix'], dtype=np.float)
        cluster_matrix = irm.infinite_relational_model(causal_matrix, body['threshold'])
        return cluster_matrix
