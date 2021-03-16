'''
Author: yangxingchen
Date: 2021-03-04 21:37:27
LastEditors: yangxingchen
LastEditTime: 2021-03-04 22:18:59
Description: 
'''

from flask import Blueprint, render_template, g


blueprint = Blueprint("admin", __name__, url_prefix="/admin", static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def admin():
    return render_template("admin/index.html")
    