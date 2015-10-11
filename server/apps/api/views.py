# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restplus import Api

app = Blueprint('api', __name__)
api = Api(app, version='1.0', title='GST API', description='GST API for Game Manager', catch_all_404s=True)

ns_users = api.namespace('users')
ns_posts = api.namespace('posts')
