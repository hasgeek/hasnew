#!/usr/bin/env python
from hasnew import app, init_for
from hasnew.models import db
init_for('dev')
db.create_all()
app.run('0.0.0.0', debug=True, port=8010)
