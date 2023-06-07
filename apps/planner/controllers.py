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

from py4web.utils.form import FormStyleBulma, Form
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user

from http import HTTPStatus

from datetime import datetime as dt

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    # rows = db(db.task.created_by == get_user()).select()
    # days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # date = dt.now()
    #return dict(rows=rows)
    return dict(
        get_tasks_url = URL('get_all_tasks', signer=url_signer),
    )

@action('get_all_tasks')
@action.uses(db, auth.user)
def get_all_tasks():
    # connect TASKS table with the AUTH_USER table using "join"
    r = db(db.task).select(join=db.auth_user.on(db.task.created_by == db.auth_user.id)).as_list()
    # print("HERE ARE THE ROWS: ", r)
    return dict(
        r=r,
        me=get_user(),
    )

@action('create_task', method="POST")
@action.uses(db, auth.user)
def create_task():
    # Implement. 
    title = request.json.get('title')
    description = request.json.get('description')
    date = request.json.get('date')
    day= request.json.get('day')
    # print("- THE TITLE OF THE TASK IS :", title, "\n- THE DESCRIPTION IS: ", description)
    db.task.insert(
        title=title,
        description=description,
        date=date,
        day=day,
    )
    db.commit()
    return "ok"

#to edit an entry
@action('edit/<task_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit.html')
def edit(task_id=None):
    assert task_id is not None
    # Check for correct permissions before editing
    if db.task[task_id] is None or not db.task[task_id].created_by == get_user():
        return HTTPStatus.BAD_REQUEST.name
    p = db.task[task_id]
    if p is None:
        # Nothing found to be edited
        redirect(URL('index'))

    #edit form, has records
    form = Form(db.task, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # The update already happened!
        redirect(URL('index'))
    return dict(form=form) # if error/empty, just return the form again
