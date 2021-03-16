'''
Author: yangxingchen
Date: 2021-02-04 11:27:47
LastEditors: yangxingchen
LastEditTime: 2021-02-04 12:25:28
Description:
'''
from flask import request, jsonify

from ablog.extensions import csrf_protect
from ablog.user.schema import UserSchema

from ablog.user.models import User, generate_token, decode_token

from ablog.utils.http_response import make_response

from flask import Blueprint

blueprint = Blueprint('auth', __name__, url_prefix="/api/v1/auth")

@blueprint.route('/signin', methods=['POST'])
@csrf_protect.exempt
def signin():
    # 登陆
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'error'})

    if not user.check_password(password):
        return jsonify({'error': '用户名或密码错误'})

    status, access_token = generate_token((user.id))
    if not status:
        return make_response(code=401, data=access_token)
    return make_response({'token': access_token})


@blueprint.route('/user_info', methods=['GET'])
def user_info():
    token = request.args['token']
    token = token.replace('Bearer ', '')
    payload = decode_token(token)
    user = User.query.filter_by(id=payload).first()
    userSchema = UserSchema()

    data = userSchema.dump(user)
    data['roles'] = ['admin']
    return jsonify({'code': 20000, 'data': data})


@blueprint.route('/signout', methods=['POST'])
@csrf_protect.exempt
def signout():
    # 登陆
    return make_response({})

