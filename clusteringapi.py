# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from clustering import irm
from constants import DATA_SIM
from constants import DATA_WILD
from constants import DATA_TRP3
from constants import DATA_TRP3_RAW

class Clustering(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        method = body['method']
        data_name = body['dataName']

        if method == 'IRM':
            window_size = body["windowSize"]
            if data_name == DATA_TRP3:
                if window_size == 3 or window_size == 5 or window_size == 7:
                    f = open("./data/clustermatrix-" + data_name + '-' + str(window_size), "r")
                    response_msg = json.load(f)
                else:
                   response_msg = self.infinite_relational_model(body)
            elif data_name == DATA_SIM:
                f = open("./data/clustermatrix-sim", "r")
                response_msg = json.load(f)
            elif data_name == DATA_WILD:
                f = open("./data/clustermatrix-data_wild", "r")
                response_msg = json.load(f)
            elif data_name == DATA_TRP3_RAW:
                f = open("./data/clustermatrix-data_trp3_raw", "r")
                response_msg = json.load(f)
                # response_msg = self.infinite_relational_model(body)
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
        window_size = body['windowSize']

        response_msg = irm.infinite_relational_model(causal_matrix, threshold, sampled_coords, data_name, window_size)
        return response_msg
