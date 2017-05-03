# -*- coding: utf-8 -*-

from __future__ import absolute_import
from flask_sqlalchemy import SQLAlchemy
from flask_commentease import Commentease
from .. import app

db = SQLAlchemy(app)
commentease = Commentease(db=db)

from .user import *
from .profile import *
from .post import *
