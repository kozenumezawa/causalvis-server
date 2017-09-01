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
            # response_msg = self.infinite_relational_model(body)
            f = open("./data/clustermatrix", "r")
            response_msg = json.load(f)
        else:
            response_msg = {
                'clusterMatrix': []
            }

        resp.body = json.dumps(response_msg)
        resp.status = falcon.HTTP_200

    @staticmethod
    def infinite_relational_model(body):
        causal_matrix = np.array(body['causalMatrix'], dtype=np.float)
        response_msg = irm.infinite_relational_model(causal_matrix, body['threshold'], body['sampledCoords'])
        return response_msg
