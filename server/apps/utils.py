# -*- coding: utf-8 -*-

from flask import g
from apps.extensions import auth, bcrypt
from apps.users.models import User


def verify_password(email, password):
    print('test')
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return bcrypt.check_password_hash(user.password, password)