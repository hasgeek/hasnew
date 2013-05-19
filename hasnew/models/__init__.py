# -*- coding: utf-8 -*-

from __future__ import absolute_import
from flask.ext.sqlalchemy import SQLAlchemy
from .. import app

db = SQLAlchemy(app)

from .user import *
from .profile import *
from .post import *
