# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse, fields, marshal_with

from apps.api.models import Post
from apps.common.argument_class import Argument
from apps.database import db
from apps.extensions import auth

post_parser = reqparse.RequestParser(argument_class=Argument)
post_parser.add_argument('title', type=str, required=True, help='Title cannot be blank!')
post_parser.add_argument('body', type=str)

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'user_id': fields.Integer,
}

class PostListAPI(Resource):

    @marshal_with(post_fields)
    def get(self):
        posts = Post.query.all()
        return posts

    @auth.login_required
    @marshal_with(post_fields)
    def post(self):
        args = post_parser.parse_args()
        post = Post(args.title, args.body)
        db.session.add(post)
        db.session.commit()
        return post


class PostAPI(Resource):

    @marshal_with(post_fields)
    def get(self, id):
        posts = Post.query.filter_by(id=id).first()
        return posts