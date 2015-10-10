# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_security import Security
security = Security()

# from flask.ext.jwt import JWT
# jwt = JWT()

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from flask_migrate import Migrate
migrate = Migrate()


