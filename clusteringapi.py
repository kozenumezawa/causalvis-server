# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from clustering import irm


class Clustering(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']
        data_name = body['dataName']

        if method == 'IRM':
            if data_name == 'real' or data_name == 'sim':
                f = open("./data/clustermatrix-" + data_name, "r")
                response_msg = json.load(f)
            else:
                response_msg = self.infinite_relational_model(body)

        else:
            response_msg = {
                'clusterMatrix': []
            }

        resp.body = json.dumps(response_msg)
        resp.status = falcon.HTTP_200

    @staticmethod
    def infinite_relational_model(body):
        causal_matrix = np.array(body['causalMatrix'], dtype=np.float)
        threshold = body['threshold']
        sampled_coords = body['sampledCoords']
        data_name = body['dataName']

        response_msg = irm.infinite_relational_model(causal_matrix, threshold, sampled_coords, data_name)
        return response_msg
