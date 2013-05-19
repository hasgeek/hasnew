# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form

__all__ = ['PostForm']


class PostForm(Form):
    title = wtf.TextField(u"Title", validators=[wtf.Required(), wtf.Length(max=250)])
    url = wtf.html5.URLField(u"URL", validators=[wtf.Optional(), wtf.url(), wtf.Length(max=2048)])
    description = wtf.TextAreaField(u"Description",
        description=u"Accepts Markdown formatting.")

    def validate_description(self, field):
        if not field.data:
            if not self.url.data:
                raise wtf.ValidationError("Either a URL or a description must be provided.")
