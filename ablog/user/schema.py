'''
Author: yangxingchen
Date: 2021-02-04 10:18:27
LastEditors: yangxingchen
LastEditTime: 2021-02-04 10:50:57
Description:
'''

from ablog.extensions import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", )
