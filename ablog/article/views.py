'''
Author: yangxingchen
Date: 2021-02-04 10:53:03
LastEditors: yangxingchen
LastEditTime: 2021-02-04 11:06:57
Description:
'''
from flask import Blueprint, render_template, g

from ablog.article.models import Article
from ablog.decorators import pagination

blueprint = Blueprint("article", __name__, url_prefix="/article", static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@blueprint.route("/<page>", defaults={'page': 1}, methods=["GET", "POST"])
@pagination
def list(page=1):
    """Home page."""
    paginate = Article.query.order_by(Article.create_at.desc()).paginate(**g.paginate)
    return render_template("article/list.html",
                           article_list=paginate.items,
                           next_page=paginate.next_num,
                           prev_page=paginate.prev_num,
                           has_next=paginate.has_next,
                           has_prev=paginate.has_prev)


@blueprint.route("/detail/<id>", methods=["GET", "POST"])
def detail(id):
    article = Article.query.filter_by(id = int(id)).first()
    next_a = Article.query.filter(id > id).first()
    return render_template("article/detail.html", article=article, next=next_a)


