# -*- coding: utf-8 -*-
"""User models."""
from datetime import datetime, timedelta

import jwt
from flask_login import UserMixin
from flask import current_app

from ablog.database import Column, PkModel, db, reference_col, relationship
from ablog.extensions import bcrypt
from ablog.settings import env, SECRET_KEY


def generate_token(user_id):
    """ Generates the access token"""

    # try:
    # set up a payload with an expiration time
    print(type(user_id))
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=600),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    # create the byte string token using the payload and the SECRET key
    jwt_string = jwt.encode(
        payload,
        SECRET_KEY,
        'HS256'
    )
    return True, jwt_string.decode('utf-8')
    # except Exception as e:
    #     # return an error in string format if an exception occurs
    #     return False, str(e)


def decode_token(token):
    """Decodes the access token from the Authorization header."""
    try:
        # try to decode the token using our SECRET variable
        payload = jwt.decode(token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        # the token is expired, return an error string
        return "Expired token. Please login to get a new token"
    except jwt.InvalidTokenError:
        # the token is invalid, return an error string
        return "Invalid token. Please register or login"


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def load_user(token):
        if not token:
            return
        t = token.replace("Bearer ", '')
        payload = decode_token(t)

        user = User.get_by_id(payload)
        if not user:
            return
        return user

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
