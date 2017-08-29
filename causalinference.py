import json
import falcon
import numpy as np

class CausalInference(object):
    def on_post(self, req, resp):
        body = json.loads(req.stream.read().decode('utf-8'))
        print np.array(body['allTimeSeries']).shape
        # msg = corr_analysis.cross_corr_analysis(body['data'], body['max_lag'], body['win_pixels'], body['win_frames'], body['width'], body['height'])
        msg = dummy_response.cross_corr_analysis(body['data'], body['max_lag'], body['win_pixels'], body['win_frames'], body['width'], body['height'])
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200