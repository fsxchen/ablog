'''
Author: yangxingchen
Date: 2021-02-04 10:07:21
LastEditors: yangxingchen
LastEditTime: 2021-02-04 12:03:54
Description:
'''

# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, jsonify
from .models import User
from .schema import UserSchema


blueprint = Blueprint("auth_api", __name__, url_prefix="/api/v1")


from flask import request
from flask import jsonify

from .models import User
from .schema import UserSchema


@blueprint.route('/user', methods=['GET'])
def list_user():
    user_list = User.query.all()

    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(user_list))


@blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User()
    user.username = data['username']
    user.password = data['password']
    return jsonify(user.save())
