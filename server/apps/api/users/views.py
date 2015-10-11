# -*- coding: utf-8 -*-
from flask import jsonify, after_this_request, Blueprint

from flask.ext.security import LoginForm, RegisterForm
from flask.ext.security.registerable import register_user
from flask.ext.security.utils import login_user
from flask_restplus import Resource, fields

from apps.api import ns_users as ns, api
from .models import user_datastore


user_parser = api.parser()
user_parser.add_argument('email', type=str, required=True, help='Email cannot be blank!')
user_parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')


user_fields = api.model('User', {
    'id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
})

create_user_fields = api.model('CreateUser', {
    'email': fields.String(discriminator=True),
    'password': fields.String(discriminator=True),
    'password_confirm': fields.String(discriminator=True),
})

session_fields = api.model('Login', {
    'email': fields.String(discriminator=True),
    'password': fields.String(discriminator=True),
})

token_fields = api.model('Token', {
    'user_id': fields.Integer,
    'authentication_token': fields.String,
    # 'duration': fields.Integer,
})


def _make_response(form, include_user=True, include_auth_token=False):
    has_errors = len(form.errors) > 0

    if has_errors:
        api.abort(400, message=form.errors)
    else:
        response = dict()
        if include_user:
            response['user_id'] = form.user.id
        if include_auth_token:
            token = form.user.get_auth_token()
            response['authentication_token'] = token

    return response


def _commit(response=None):
    user_datastore.commit()
    return response


@ns.route('/')
class UserAPI(Resource):

    @api.expect(create_user_fields, validate=True)
    @api.response(400, 'Validation Error')
    @api.marshal_with(user_fields, code=201)
    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            user = register_user(**form.to_dict())
            form.user = user

        return _make_response(form, include_auth_token=True)


@ns.route('/token')
class TokenAPI(Resource):

    @api.expect(session_fields, validate=True)
    @api.response(400, 'Validation Error')
    @api.marshal_with(token_fields)
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            login_user(form.user, remember=False)
            after_this_request(_commit)

        return _make_response(form, include_auth_token=True)

