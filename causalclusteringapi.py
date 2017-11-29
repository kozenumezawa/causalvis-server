# -*- coding: utf-8 -*-

import json
import falcon
import numpy as np

from causalinference import allcrosscorr
from constants import DATA_SIM
from constants import DATA_WILD
from constants import DATA_TRP3
from constants import DATA_TRP3_RAW

from clustering import irm

class CausalClustering(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))

        # conduct causal inference
        causal_method = body['causalMethod']
        data_name = body['dataName']

        if causal_method == 'GRANGER':
            corr_list = self.create_granger_matrix(body)
        elif causal_method == 'CCM':
            print ('ccm')
        elif causal_method == 'CROSS':
            window_size = body["windowSize"]
            if data_name == DATA_TRP3:
                if window_size == 3 or window_size == 5 or window_size == 7:
                    f = open("./data/corr_list-" + data_name + '-' + str(window_size), "r")
                    corr_list = json.load(f)
                    f = open("./data/lag_list-" + data_name + '-' + str(window_size), "r")
                    lag_list = json.load(f)
                else:
                    corr_list, lag_list = self.create_cross_matrix(body)
            elif data_name == DATA_SIM:
                # corr_list, lag_list = self.create_cross_matrix(body)
                f = open("./data/corr_list-" + data_name + '-3', "r")
                corr_list = json.load(f)
                f = open("./data/lag_list-" + data_name + '-3', "r")
                lag_list = json.load(f)
            elif data_name == DATA_WILD:
                corr_list, lag_list = self.create_cross_matrix(body)
            elif data_name == DATA_TRP3_RAW:
                corr_list, lag_list = self.create_cross_matrix(body)
            else:
                corr_list, lag_list = self.create_cross_matrix(body)
        else:
            corr_list = []

        corr_matrix = corr_list
        lag_matrix = lag_list


        # conduct clustering
        clustering_method = body['clusteringMethod']
        data_name = body['dataName']

        if clustering_method == 'IRM':
            window_size = body["windowSize"]
            if data_name == DATA_TRP3:
                if window_size == 3 or window_size == 5 or window_size == 7:
                    f = open("./data/clustermatrix-" + data_name + '-' + str(window_size), "r")
                    response_msg = json.load(f)
                else:
                    response_msg = self.infinite_relational_model(body, corr_matrix, lag_matrix)
            elif data_name == DATA_SIM:
                # response_msg = self.infinite_relational_model(body, corr_matrix, lag_matrix)
                f = open("./data/clustermatrix-data_sim-3", "r")
                response_msg = json.load(f)
            elif data_name == DATA_WILD:
                response_msg = self.infinite_relational_model(body, corr_matrix, lag_matrix)
            elif data_name == DATA_TRP3_RAW:
                response_msg = self.infinite_relational_model(body, corr_matrix, lag_matrix)
            else:
                response_msg = self.infinite_relational_model(body, corr_matrix, lag_matrix)
            response_msg = self.sort(response_msg)

        else:
            response_msg = {
                'clusterMatrix': [],
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
        max_lag = body['maxLag']
        lag_step = body['lagStep']
        data_name = body['dataName']
        window_size = body['windowSize']

        corr_list, lag_list = allcrosscorr.calc_all(all_time_series,  max_lag, lag_step, data_name, window_size)
        return (corr_list, lag_list)


    @staticmethod
    def infinite_relational_model(body, corr_matrix, lag_matrix):
        corr_matrix = np.array(corr_matrix, dtype=np.float)
        lag_matrix = np.array(lag_matrix, dtype=np.float)
        threshold = body['threshold']
        sampled_coords = body['sampledCoords']
        data_name = body['dataName']
        window_size = body['windowSize']

        response_msg = irm.infinite_relational_model(corr_matrix, lag_matrix, threshold, sampled_coords, data_name, window_size)
        return response_msg

    @staticmethod
    def sort(json_data):
        corr_matrix = np.array(json_data['corrMatrix'])
        lag_matrix = np.array(json_data['lagMatrix'])
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
                if effect_cluster_range == causal_cluster_range:
                    row.append(False)
                    continue
                # count the number of connections between two clusters
                causal_cnt = 0
                for causal_idx in range(causal_cluster_range['start'], causal_cluster_range['end']):
                    for effect_idx in range(effect_cluster_range['start'], effect_cluster_range['end']):
                        if cluster_matrix[causal_idx][effect_idx] == True:
                            causal_cnt += 1
                width = effect_cluster_range['end'] - effect_cluster_range['start']
                area = width * height
                if causal_cnt > area * 0.9:
                    row.append(True)
                    continue
                row.append(False)
            adjacency_matrix.append(row)

        # count the number of source and target
        n_sources = [row.count(True) for row in adjacency_matrix]
        adjacency_matrix_T = map(list, zip(*adjacency_matrix))
        n_targets = [col.count(True) for col in adjacency_matrix_T]

        # calculate difference between nTargets and nSources
        n_diffs = [n_source - n_target for (n_source, n_target) in zip(n_sources, n_targets)]
        n_diffs = np.array(n_diffs)

        cluster_order = n_diffs.argsort()
        cluster_order = cluster_order[::-1]

        # get new index after sorting
        new_order = []
        for (new_cluster_idx, old_cluster_idx) in enumerate(cluster_order):
            start = cluster_range_list[old_cluster_idx]['start']
            end = cluster_range_list[old_cluster_idx]['end']
            for new_idx in range(start, end):
                new_order.append(new_idx)

        # update the order of matrix according to the sorting result
        corr_matrix = corr_matrix[new_order]
        corr_matrix = corr_matrix[:, new_order]

        lag_matrix = lag_matrix[new_order]
        lag_matrix = lag_matrix[:, new_order]


        cluster_matrix = cluster_matrix[new_order]
        cluster_matrix = cluster_matrix[:, new_order]
        cluster_sampled_coords = cluster_sampled_coords[new_order]
        ordering = ordering[new_order]
        n_cluster_list = n_cluster_list[cluster_order]

        response_msg = {
            'corrMatrix': corr_matrix.tolist(),
            'lagMatrix': lag_matrix.tolist(),
            'clusterMatrix': cluster_matrix.tolist(),
            'clusterSampledCoords': cluster_sampled_coords.tolist(),
            'nClusterList': n_cluster_list.tolist(),
            'ordering': ordering.tolist(),
        }
        return response_msg

