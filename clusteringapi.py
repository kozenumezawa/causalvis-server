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
            response_msg = self.sort(response_msg)

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

    @staticmethod
    def sort(json_data):
        cluster_matrix = np.array(json_data['clusterMatrix'])
        cluster_sampled_coords = np.array(json_data['clusterSampledCoords'])
        n_cluster_list = np.array(json_data['nClusterList'])
        ordering = np.array(json_data['ordering'])

        cluster_range_list = []
        end_idx = 0
        for n_cluster in n_cluster_list:
            start_idx = end_idx
            end_idx = start_idx + n_cluster
            cluster_range_list.append({
                'start': start_idx,
                'end': end_idx
            })

        adjacency_matrix = []
        for causal_cluster_range in cluster_range_list:
            height = causal_cluster_range['end'] - causal_cluster_range['start']
            row = []
            for effect_cluster_range in cluster_range_list:
                if causal_cluster_range



#         const adjacencyMatrix = clusterRangeList.map((causalClusterRange) => {
#             const height = causalClusterRange.end - causalClusterRange.start;
#         return clusterRangeList.map((effectClusterRange) => {
#         if (causalClusterRange === effectClusterRange) {
#         return false;
#         }
#         // count the number of connections between two clusters
#         let causalCnt = 0;
#         for (let causalIdx = causalClusterRange.start; causalIdx < causalClusterRange.end; causalIdx += 1) {
#         for (let effectIdx = effectClusterRange.start; effectIdx < effectClusterRange.end; effectIdx += 1) {
#         if (clusterMatrices[dataIdx][causalIdx][effectIdx] === true) {
#         causalCnt += 1;
#         }
#         }
#     }
#     const width = effectClusterRange.end - effectClusterRange.start;
#     const area = width * height;
#     if (causalCnt > area * 0.9) {
#     return true;
# }
# return false;
# });
# });
#
#
        return json_data
