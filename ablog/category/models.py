'''
Author: yangxingchen
Date: 2021-03-04 23:22:29
LastEditors: yangxingchen
LastEditTime: 2021-03-04 23:23:00
Description: 
'''

from ablog.extensions import db
from ablog.database import BaseModel, reference_col, relationship

class Category(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    articles = db.relationship('Article', backref='category')