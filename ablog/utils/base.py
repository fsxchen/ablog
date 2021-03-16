'''
Author: yangxingchen
Date: 2021-02-04 11:17:52
LastEditors: yangxingchen
LastEditTime: 2021-02-04 11:18:03
Description:
'''
from flask_sqlalchemy import Pagination
from datetime import datetime

from ablog.extensions import db, ma


class BaseModel(db.Model):
    __abstract__ = True

    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)
    delete_at = db.Column(db.DateTime, default=datetime.now)


class PaginateSchema(ma.Schema):
    class Meta:
        fields = ("has_next", "has_prev", "total", "next_num", "page",
                  "pages", "per_page", "pre_num")


def get_page_json(paginate: Pagination):
    paginate_schema = PaginateSchema()
    return paginate_schema.dump(paginate)
