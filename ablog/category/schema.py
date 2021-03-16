'''
Author: yangxingchen
Date: 2021-02-04 10:58:46
LastEditors: yangxingchen
LastEditTime: 2021-03-05 17:43:39
Description:
'''
from ablog.extensions import ma
from ablog.user.schema import UserSchema
from marshmallow import fields


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'create_at')

