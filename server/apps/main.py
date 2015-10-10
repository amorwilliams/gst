# -*- coding:utf-8 -*-

import os
import sys

from flask.ext.security.utils import verify_password

from apps.users.models import user_datastore

from base import BaseApp
from extensions import security, migrate
from database import db


# apps is a special folder where you can place your blueprints
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))

basestring = getattr(__builtins__, 'basestring', str)


class App(BaseApp):
    def configure_database(self):
        """
        Database configuration should be set here
        """
        db.init_app(self)

    def configure_extensions(self):
        # flask-migrate
        migrate.init_app(self, db)

        # flask_cors
        from flask_cors import CORS
        CORS(self, resources={r'/api/*': {'origins': '*'}})

        # flask-security
        security.init_app(self, datastore=user_datastore, register_blueprint=True)

        # flask-jwt
        # jwt.init_app(self)
        #
        # @jwt.authentication_handler
        # def authenticate(email, password):
        #     user = user_datastore.find_user(email=email)
        #     if user and email == user.email and verify_password(password, user.password):
        #         return user
        #     return None
        #
        # @jwt.user_handler
        # def load_user(payload):
        #     user = user_datastore.find_user(id=payload['user_id'])
        #     return user

    def configure_views(self):
        pass

def config_str_to_obj(cfg):
    if isinstance(cfg, basestring):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def app_factory(config, app_name, blueprints=None):
    # you can use Empty directly if you wish
    app = App(app_name)
    config = config_str_to_obj(config)

    app.configure(config)
    app.add_blueprint_list(blueprints or config.BLUEPRINTS)
    app.setup()

    return app
