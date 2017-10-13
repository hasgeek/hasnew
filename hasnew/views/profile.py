# -*- coding: utf-8 -*-

from flask import g
from coaster.views import load_model, render_with
from .. import app
from ..models import db, Profile, UserProfileVisit


@app.route('/<profile>')
@render_with('profile.html.jinja2')
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_view(profile):
    if g.user:
        visit = UserProfileVisit.get(g.user, profile)
        visit.update()
        db.session.commit()
    return {'profile': profile}
