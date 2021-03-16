'''
Author: yangxingchen
Date: 2021-02-03 21:57:51
LastEditors: yangxingchen
LastEditTime: 2021-03-05 17:34:26
Description:
'''
# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template, request, g

from ablog import (
    commands,
    public,
    user,
    auth,
    article,
    category,
    admin,
)
from ablog.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    cors,
    db,
    ma,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)


def create_app(config_object="ablog.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    registr_apis(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    before_request(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(article.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(category.api.blueprint)
    return None


def registr_apis(app):
    """Register Flask api"""
    app.register_blueprint(user.api.blueprint)
    app.register_blueprint(article.api.blueprint)
    app.register_blueprint(auth.api.blueprint)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def before_request(app):
    def user_info():
        from ablog.user.models import User
        token = request.headers.get("Authorization")
        if token:
            user = User.load_user(token)
            if not user:
                return
            g.user = user

    app.before_request(user_info)
