# -*- coding: utf-8 -*-
from datetime import datetime
from flask import after_this_request, request
from flask.ext.security import login_user
from apps.users.models import user_datastore


# def _commit(response=None):
#     user_datastore.commit()
#     return response
#
# def login(user):
#     if 'X-Forwarded-For' not in request.headers:
#         remote_addr = request.remote_addr or 'untrackable'
#     else:
#         remote_addr = request.headers.getlist("X-Forwarded-For")[0]
#
#     old_current_login, new_current_login = user.current_login_at, datetime.utcnow()
#     old_current_ip, new_current_ip = user.current_login_ip, remote_addr
#
#     user.last_login_at = old_current_login or new_current_login
#     user.current_login_at = new_current_login
#     user.last_login_ip = old_current_ip or new_current_ip
#     user.current_login_ip = new_current_ip
#     user.login_count = user.login_count + 1 if user.login_count else 1
#     after_this_request(_commit)





