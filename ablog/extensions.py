'''
Author: yangxingchen
Date: 2021-02-03 21:57:51
LastEditors: yangxingchen
LastEditTime: 2021-02-04 11:37:40
Description: 
'''
# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_marshmallow import Marshmallow

bcrypt = Bcrypt()
cors = CORS()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
ma = ma = Marshmallow()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
