# -*- coding:utf-8 -*-

import os
import sys
from base import BaseApp

from extensions import bcrypt, migrate, ma, auth
from database import db
from utils import verify_password

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

    def configure_views(self):
        pass

    def configure_extensions(self):
        # flask_bcrypt
        bcrypt.init_app(self)

        # flask_migrate
        migrate.init_app(self, db)

        # flask_marshmallow
        ma.init_app(self)

        # flask_cors
        from flask_cors import CORS
        CORS(self, resources={r'/api/*': {'origins': '*'}})

        # flask_httpauth
        @auth.verify_password
        def verify_pw(username, password):
            return verify_password(username, password)


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
