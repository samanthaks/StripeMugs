from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from .. import app
from ..models import username_table, userid_table


auth = Blueprint('auth', __name__)


def authenticate(username, password):
    user = username_table.get(username, None)
    print(user)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    print(user_id)
    return userid_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)

@auth.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity
