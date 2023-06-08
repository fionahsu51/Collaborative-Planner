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
    return dict(
        get_tasks_url = URL('get_all_tasks', signer=url_signer),
        get_users_url = URL('get_users', signer=url_signer),
        invite_url=URL('set_invite', signer=url_signer),
    )

@action('get_users')
@action.uses(db, auth.user, url_signer)
def get_users():
    users = db(db.auth_user).select(db.auth_user.ALL).as_list()


    # row = db((db.invitation.group_id == request.params.get('user_id'))
    #          & (db.follow.created_by == get_user())).select().first()
    # status = row.status if row is not None else False
    # u = []
    # for user in users:
    #     new_user = user['auth_user']
    #     new_user['status'] = user['follow']['status']
    #     u.append(new_user)
    
    return dict(
        users=users,
        me=get_user()
    )

@action("set_invite", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def set_invite():
    group_id = request.json.get('user_id')
    status = request.json.get('status')
    db.invitation.update_or_insert( 
        ((db.invitation.group_id==group_id) & (db.invitation.created_by==get_user())),
        group_id=group_id,
        status=status
    )
    return "ok"

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
    invited_users = request.json.get('invited_users')
    # print("- THE TITLE OF THE TASK IS :", title, "\n- THE DESCRIPTION IS: ", description)
    db.task.insert(
        title=title,
        description=description,
        date=date,
        day=day,
        invited_users=invited_users
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

@action('delete/<task_id:int>')
@action.uses(db, session, auth.user)
def delete(task_id=None):
    assert task_id is not None
    # Check for correct permissions before editing
    if db.task[task_id] is None or not db.task[task_id].created_by == get_user():
        return HTTPStatus.BAD_REQUEST.name
    db(db.task.id == task_id).delete()
    redirect(URL('index'))