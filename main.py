# -*- coding: utf-8 -*-

import falcon

from causalclusteringapi import CausalClustering

class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

api = falcon.API(middleware=[CORSMiddleware()])

api.add_route('/api/v1/causal-and-clustering', CausalClustering())

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("127.0.0.1", 3000, api)
    httpd.serve_forever()
