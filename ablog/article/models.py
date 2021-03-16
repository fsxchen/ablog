'''
Author: yangxingchen
Date: 2021-02-04 10:53:30
LastEditors: yangxingchen
LastEditTime: 2021-03-04 23:21:54
Description:
'''
import enum

from ablog.extensions import db
from ablog.database import BaseModel, reference_col, relationship


class PublishStatusEnum(enum.Enum):
    published = 'published'
    draft = 'draft'
    deleted = 'deleted'


class Article(BaseModel):
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    content_md = db.Column(db.Text())
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="articles")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    status = db.Column(db.Enum(PublishStatusEnum), default=PublishStatusEnum.published)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
