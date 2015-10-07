# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.restful import Api

from apps.api.post import PostListAPI
from apps.api.post import PostAPI
from apps.api.user import UserAPI, SessionAPI

app = Blueprint('api', __name__)
api = Api(app, catch_all_404s=True)

api.add_resource(UserAPI, '/users')
api.add_resource(SessionAPI, '/sessions')
api.add_resource(PostListAPI, '/posts')
api.add_resource(PostAPI, '/posts/<int:id>')