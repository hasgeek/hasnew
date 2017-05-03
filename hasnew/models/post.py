# -*- coding: utf-8 -*-

from flask import Markup, url_for
from flask_commentease import VotingMixin, CommentingMixin
from coaster.sqlalchemy import TimestampMixin, BaseScopedIdNameMixin
from coaster.gfm import markdown
from . import db
from .user import User
from .profile import Profile

__all__ = ['Post', 'UserPostVisit']


class Post(VotingMixin, CommentingMixin, BaseScopedIdNameMixin, db.Model):
    """A post"""
    __tablename__ = 'post'
    profile_id = db.Column(None, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile, backref=db.backref('posts',
        cascade='all, delete-orphan', lazy='dynamic'))
    parent = db.synonym('profile')

    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('posts',
        cascade='all, delete-orphan', lazy='dynamic'))

    url = db.Column(db.Unicode(2048), nullable=True)
    _description = db.Column('description', db.UnicodeText, default=u'', nullable=False)
    _description_html = db.Column('description_html', db.UnicodeText, default=u'', nullable=False)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        self._description_html = markdown(value)

    @property
    def description_html(self):
        return Markup(self._description_html)

    def permissions(self, user, inherited=None):
        perms = super(Post, self).permissions(user, inherited)
        perms.add('view')
        if user is not None:
            if user == self.user or self.profile.userid in user.user_organizations_owned_ids():
                perms.add('edit')
                perms.add('delete')
        return perms

    def url_for(self, action='view', _external=False):
        if action == 'view':
            return url_for('post_view', profile=self.profile.name, post=self.url_name, _external=_external)
        elif action == 'edit':
            return url_for('post_edit', profile=self.profile.name, post=self.url_name, _external=_external)
        elif action == 'delete':
            return url_for('post_delete', profile=self.profile.name, post=self.url_name, _external=_external)
        elif action == 'vote':
            return url_for('post_vote', profile=self.profile.name, post=self.url_name, _external=_external)
        elif action == 'comments':
            return url_for('post_comment', profile=self.profile.name, post=self.url_name, _external=_external)


class UserPostVisit(TimestampMixin, db.Model):
    __tablename__ = 'user_post_visit'
    user_id = db.Column(None, db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    user = db.relationship(User)
    post_id = db.Column(None, db.ForeignKey('post.id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    post = db.relationship(Post)

    visited = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def get(cls, user, post):
        instance = cls.query.get((user.id, post.id))
        if instance is None:
            instance = cls(user=user, post=post)
            db.session.add(instance)
        return instance

    def update(self):
        """Update the last visited timestamp."""
        self.updated_at = db.func.now()
