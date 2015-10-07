# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse, fields, marshal_with

from apps.api.models import User
from apps.common.argument_class import Argument
from apps.database import db
from apps.extensions import bcrypt

user_parser = reqparse.RequestParser(argument_class=Argument)
user_parser.add_argument('email', type=str, required=True, help='Email cannot be blank!')
user_parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
}

class UserAPI(Resource):

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        password_hash = bcrypt.generate_password_hash(args.password)
        user = User(args.email, password_hash)
        db.session.add(user)
        db.session.commit()
        return user


class SessionAPI(Resource):

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user and bcrypt.check_password_hash(user.password, args.password):
            return user
        return '', 401