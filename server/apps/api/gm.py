# -*- coding: utf-8 -*-

from flask.ext.restful import Resource

import requests

class GameUserAPI(Resource):

    def get(self):
        requests.get('http://192.168.1.210/')