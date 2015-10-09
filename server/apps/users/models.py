# -*- coding: utf-8 -*-

import flask
from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, SignatureExpired, BadSignature)

from apps.database import db
from apps.extensions import bcrypt


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<models.User[email=%s]>' % self.email

    # def hash_password(self, password):
    #     self.password = bcrypt.generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return bcrypt.check_password_hash(self.password, password)
    #
    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(flask.current_app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id})
    #
    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(flask.current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None    # valid token, but expired
    #     except BadSignature:
    #         return None    # invalid token
    #     user = User.query.get(data['id'])
    #     return user


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class SomeStuff(db.Model):
    __tablename__ = 'somestuff'
    id = db.Column(db.Integer, primary_key=True)
    data1 = db.Column(db.Integer)
    data2 = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship(User, lazy='joined', join_depth=1, viewonly=True)