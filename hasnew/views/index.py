# -*- coding: utf-8 -*-

from coaster.views import render_with
from .. import app
from ..models import Post


@app.route('/')
@render_with('index.html.jinja2')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).limit(100).all()
    return {'posts': posts}
