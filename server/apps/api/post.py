# -*- coding: utf-8 -*-

from flask_restplus import Resource, fields

from apps.database import db
from apps.extensions import auth

from .models import Post
from .urls import api


post_parser = api.parser()
post_parser.add_argument('title', type=str, required=True, help='Title cannot be blank!')
post_parser.add_argument('body', type=str)

post_fields = api.model('Post', {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'user_id': fields.Integer,
})

create_post_fields = api.model('CreatePost', {
    'title': fields.String,
    'body': fields.String,
})


@api.route('/posts')
class PostListAPI(Resource):

    @api.marshal_list_with(post_fields)
    def get(self):
        posts = Post.query.all()
        return posts

    @api.expect(create_post_fields)
    @auth.login_required
    @api.marshal_with(post_fields)
    def post(self):
        args = post_parser.parse_args()
        post = Post(args.title, args.body)
        db.session.add(post)
        db.session.commit()
        return post


@api.route('/posts/<int:id>')
class PostAPI(Resource):

    @api.doc(params={'id': 'Post ID'})
    @api.marshal_with(post_fields)
    def get(self, id):
        posts = Post.query.filter_by(id=id).first()
        if not posts:
            api.abort(404)
        return posts

