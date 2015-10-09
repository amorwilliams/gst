# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_security import Security
security = Security()

from flask_jwt import JWT
jwt = JWT()

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from flask_migrate import Migrate
migrate = Migrate()


