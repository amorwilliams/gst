# -*- coding:utf-8 -*-

import os
import sys

from apps.api.users import user_datastore

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
