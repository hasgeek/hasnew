# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive
from __future__ import absolute_import
from flask import Flask
from flask_lastuser import Lastuser
from flask_lastuser.sqlalchemy import UserManager
from baseframe import baseframe, assets, Version
import coaster.app

version = Version('0.1.0')

# First, make an app

app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()

# Second, import the models and views

from . import models, views
from .models import db, commentease

# Third, setup baseframe and assets

assets['hasnew.js'][version] = 'js/app.js'
assets['hasnew.css'][version] = 'css/app.css'


# Configure the app
def init_for(env):
    coaster.app.init_app(app, env)
    baseframe.init_app(app, requires=['baseframe', 'commentease', 'hasnew'])
    commentease.init_app(app)
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(db, models.User))
