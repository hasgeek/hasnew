# -*- coding: utf-8 -*-

from flask import g, flash
from coaster.views import load_model, load_models, render_with
from baseframe.forms import render_form, render_redirect, render_delete_sqla
from .. import app, lastuser
from ..models import db, Profile, Post, UserPostVisit
from ..forms import PostForm


@app.route('/<profile>/<post>')
@render_with('post.html')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Post, {'url_name': 'post', 'profile': 'profile'}, 'post')
    )
def post_view(profile, post):
    if g.user:
        visit = UserPostVisit.get(g.user, post)
        visit.visited = True
        visit.update()
        db.session.commit()
    return {'profile': profile, 'post': post}


@app.route('/<profile>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile', permission='new')
def post_new(profile):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(profile=profile, user=g.user)
        form.populate_obj(post)
        post.make_name()
        db.session.add(post)
        db.session.commit()
        flash(u"New post added", 'success')
        # TODO: Raise a signal for the twitter feed handler
        return render_redirect(post.url_for(), code=303)
    return render_form(form=form, title=u"New post", cancel_url=profile.url_for(), ajax=False)


@app.route('/<profile>/<post>/edit', methods=['GET', 'POST'])
@app.route('/<profile>/<post>', methods=['PUT'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Post, {'url_name': 'post', 'profile': 'profile'}, 'post'),
    permission='edit')
def post_edit(profile, post):
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        post.make_name()
        db.session.commit()
        flash(u"Post has been edited", 'success')
        # TODO: Raise an edit signal here
        return render_redirect(post.url_for(), code=303)
    return render_form(form=form, title=u"Edit post", cancel_url=post.url_for(), ajax=False)


@app.route('/<profile>/<post>/delete', methods=['GET', 'POST'])
@app.route('/<profile>/<post>', methods=['DELETE'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Post, {'url_name': 'post', 'profile': 'profile'}, 'post'),
    permission='delete')
def post_delete(profile, post):
    # TODO: How do we raise a signal here?
    return render_delete_sqla(post, db, title=u"Delete post?",
        message=u"Deleting a post will also delete all comments permanently. There is no undo.",
        success=u"Post has been deleted",
        next=profile.url_for(), cancel_url=post.url_for())
