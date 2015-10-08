# -*- coding: utf-8 -*-

from flask_restplus import Resource, fields

from apps.database import db
from apps.extensions import bcrypt
from apps.users.models import User

from .urls import api


user_parser = api.parser()
user_parser.add_argument('email', type=str, required=True, help='Email cannot be blank!')
user_parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')

create_user_parser = user_parser.copy()
create_user_parser.add_argument('username', type=str, required=True, help='Username cannot be blank!')
create_user_parser.add_argument('first_name', type=str, required=True, help='First name cannot be blank!')
create_user_parser.add_argument('last_name', type=str, required=True, help='Last name cannot be blank!')


user_fields = api.model('User', {
    'id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
})

create_user_fields = api.model('CreateUser', {
    'email': fields.String(discriminator=True),
    'username': fields.String(discriminator=True),
    'first_name': fields.String(discriminator=True),
    'last_name': fields.String(discriminator=True),
    'password': fields.String(discriminator=True),
})

session_fields = api.model('Login', {
    'email': fields.String(discriminator=True),
    'password': fields.String(discriminator=True),
})


@api.route('/users')
class UserAPI(Resource):

    @api.expect(create_user_fields, validate=True)
    @api.response(201, 'Success')
    @api.response(400, 'Validation Error')
    @api.marshal_with(user_fields, code=201)
    def post(self):
        args = create_user_parser.parse_args()
        password_hash = bcrypt.generate_password_hash(args.password)
        user = User(args.username, args.email, password_hash)
        user.first_name = args.first_name
        user.last_name = args.last_name
        db.session.add(user)
        db.session.commit()
        return user


@api.route('/sessions')
class SessionAPI(Resource):

    @api.expect(session_fields, validate=True)
    @api.response(200, 'Success')
    @api.response(401, 'Validation Error')
    @api.marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user and bcrypt.check_password_hash(user.password, args.password):
            return user
        api.abort(401, 'Failed to create session!')