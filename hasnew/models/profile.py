# -*- coding: utf-8 -*-

from flask import url_for
from coaster.sqlalchemy import TimestampMixin, BaseNameMixin
from flask.ext.lastuser.sqlalchemy import ProfileMixin
from . import db
from .user import User

__all__ = ['Profile', 'UserProfileVisit']


class Profile(ProfileMixin, BaseNameMixin, db.Model):
    """
    User profiles.
    """
    __tablename__ = 'profile'
    userid = db.Column(db.Unicode(22), nullable=False, unique=True)

    def permissions(self, user, inherited=None):
        perms = super(Profile, self).permissions(user, inherited)
        if user and self.userid in user.user_organizations_owned_ids():
            perms.add('new-post')
        return perms

    def url_for(self, action='view', _external=False):
        if action == 'view':
            return url_for('profile_view', profile=self.name, _external=_external)
        elif action == 'new-post':
            return url_for('post_new', profile=self.name, _external=_external)


class UserProfileVisit(TimestampMixin, db.Model):
    """
    Date when user last visited a profile.
    """
    __tablename__ = 'user_profile_visit'
    user_id = db.Column(None, db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    user = db.relationship(User)
    profile_id = db.Column(None, db.ForeignKey('profile.id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    profile = db.relationship(Profile)

    @classmethod
    def get(cls, user, profile):
        instance = cls.query.get((user.id, profile.id))
        if instance is None:
            instance = cls(user=user, profile=profile)
            db.session.add(instance)
        return instance

    def update(self):
        """Update the last visited timestamp."""
        self.updated_at = db.func.now()
