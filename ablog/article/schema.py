'''
Author: yangxingchen
Date: 2021-02-04 10:58:46
LastEditors: yangxingchen
LastEditTime: 2021-03-04 23:25:57
Description:
'''
from ablog.extensions import ma
from ablog.user.schema import UserSchema
from ablog.category.schema import CategorySchema
from marshmallow import fields



class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content", "create_at", "user", "content_md",
                  "status", "category")
    status = fields.Method("get_status")

    def get_status(self, obj):
        return obj.status.value

    user = ma.Nested(UserSchema)
    category = ma.Nested(CategorySchema)
