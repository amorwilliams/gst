# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_migrate import Migrate
migrate = Migrate()

from flask_restful import Api
from flask_restful_swagger import swagger
api = swagger.docs(Api(), apiVersion='0.1')

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from flask_marshmallow import Marshmallow
ma = Marshmallow()

