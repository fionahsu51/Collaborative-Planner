"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    get_tasks_url = URL('get_all_tasks', signer=url_signer),
    # rows = db(db.task.created_by == get_user()).select()
    return dict(get_tasks_url=get_tasks_url)

@action("get_all_tasks")
@action.uses(db, auth.user)
def get_all_tasks():
    r = db(db.task).select(join=db.auth_user.on(db.task.created_by == db.auth_user.id)).as_list()
    # print("HERE ARE THE PEOPLE IM FOLLOWING", f)
    return dict(
        r=r,
        )


@action("create_task", method="POST")
@action.uses(db, auth.user)
def create_task():
    # Implement. 
    title = request.json.get('title')
    description = request.json.get('description')
    db.task.insert(
        title=title,
        description=description
    )
    db.commit()
    return "ok"