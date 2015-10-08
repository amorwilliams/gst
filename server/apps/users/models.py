# -*- coding: utf-8 -*-

import flask
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, SignatureExpired, BadSignature)
from wtforms.validators import Email

from apps.common.sqlalchemy import BaseMixin
from apps.database import db
from apps.extensions import bcrypt


class User(BaseMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80), nullable=False)

    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    tag_line = db.Column(db.String(140))

    is_admin = db.Column(db.Boolean(), default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r & Email %r>' % self.username, self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        Simplest possible answer: All admins are staff
        """
        return self.is_admin

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(flask.current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(flask.current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user
