"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'task',
    Field('title', requires=IS_NOT_EMPTY()),
    Field('description'),
    Field('day_selected'),
    auth.signature
)

db.define_table(
    'day',
    Field('day_name'),
    auth.signature
)

db.commit()
