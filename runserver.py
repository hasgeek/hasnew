#!/usr/bin/env python
from hasnew import app, init_for
init_for('dev')
app.run('0.0.0.0', debug=True, port=8010)
