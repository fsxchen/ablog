'''
Author: yangxingchen
Date: 2021-02-04 10:59:23
LastEditors: yangxingchen
LastEditTime: 2021-03-05 18:02:28
Description:
'''


from datetime import datetime
import markdown

from flask import jsonify, request, g, Blueprint
from ablog.extensions import db, csrf_protect

from ablog.category.models import Category
from ablog.category.schema import CategorySchema

from .models import Article
from .schema import ArticleSchema
from .models import PublishStatusEnum
from ablog.utils.http_response import make_response

from ablog.utils.base import get_page_json
from ablog.decorators import login_required, pagination

blueprint = Blueprint("article_api", __name__, url_prefix="/api/v1")


@blueprint.route('/article', methods=['GET'])
@pagination
@csrf_protect.exempt
def list_article():
    paginate = Article.query.paginate(**g.paginate)
    article_schema = ArticleSchema(many=True)
    return make_response({
                    "results": article_schema.dump(paginate.items),
                    "paginate": get_page_json(paginate)
                    })


@blueprint.route('/article', methods=['POST'])
@login_required
@csrf_protect.exempt
def create_article():
    data = request.get_json()
    # 根据是否有id来判断行为是否为更新
    if data.get("id"):
        article = Article.query.filter_by(id=data['id']).first()
        if data.get('content_md'):
            article.content_md = data['content_md']
            article.content = markdown.markdown(data.get('content_md'))
        else:
            article.content = data['content']
        article.title = data['title']
        article.update_at = datetime.now()
        article.status = PublishStatusEnum(data['status'])
        article.category_id = int(data['category'])
        db.session.commit()

    else:
        article = Article()
        article.title = data['title']
        if data.get('content_md'):
            article.content_md = data['content_md']
            article.content = markdown.markdown(data.get('content_md'))
        else:
            article.content = data['content']
        article.user_id = g.user.id
        article.category_id = int(data['category'])

        db.session.add(article)
        db.session.commit()

    article_schema = ArticleSchema()

    return make_response(article_schema.dump(article))


@blueprint.route('/article/<id>', methods=['GET'])
def detail_article(id):
    article = Article.query.filter_by(id=id).first()
    article_schema = ArticleSchema()
    return make_response(article_schema.dump(article))


@blueprint.route('/category', methods=['GET'])
def list_category():
    categories = Category.query.all()
    category_schema = CategorySchema(many=True)
    return jsonify({"code": 20000,
                    "results": category_schema.dump(categories),
                    "total": 10,
                    })


@blueprint.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    # TODO name不能重复

    created_category = Category()
    create_category.name = data['name']

    created_category.save()
    category_schema = CategorySchema()
    return make_response(category_schema.dump(created_category))
