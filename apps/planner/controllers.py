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
        get_users_url = URL('get_users', signer=url_signer),
        get_tasks_url = URL('get_all_tasks', signer=url_signer),
        get_projects_url = URL('get_all_projects', signer=url_signer),
    )

@action('get_users')
@action.uses(db, auth.user, url_signer)
def get_users():
    users = db(db.auth_user).select(db.auth_user.ALL).as_list()

    return dict(
        users=users,
        me=get_user()
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

@action('get_all_projects')
@action.uses(db, auth.user)
def get_all_projects():
    r = db(db.project).select().as_list()
    return dict(
        r=r,
    )

@action('create_project', method="POST")
@action.uses(db, auth.user)
def create_project():
    name = request.json.get('name')
    color = request.json.get('color')
    db.project.insert(
        name=name,
        color=color,
    )
    db.commit()
    return "ok"

@action('create_task', method="POST")
@action.uses(db, auth.user)
def create_task():
    # Implement. 
    title = request.json.get('title')
    description = request.json.get('description')
    date = request.json.get('date')
    invited_users = request.json.get('invited_users')
    new_project = request.json.get('new_project')
    project = request.json.get('project')
    project_color = request.json.get('project_color');

    # If a new project was inserted
    if (new_project): 
        project = db(db.project).select().last()
        project = project.id + 1

    # print("- THE TITLE OF THE TASK IS :", title, "\n- THE DESCRIPTION IS: ", description)
    db.task.insert(
        title=title,
        description=description,
        date=date,
        invited_users=invited_users,
        project=project,
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

    
    # if request.method == "Post":
    #     return dict()
    # else:
    #     print("Title:", request.json.get('title'), "Desciption:", request.json.get('description'), "Date:", request.json.get('day'))
    #     redirect(URL('index'))
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

@action('edit_project/<project_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit_project.html')
def edit_project(project_id=None):
    assert project_id is not None
    # Check for correct permissions before editing
    if db.project[project_id] is None or not db.project[project_id].created_by == get_user():
        return HTTPStatus.BAD_REQUEST.name
    p = db.project[project_id]
    if p is None:
        # Nothing found to be edited
        redirect(URL('index'))

    form = Form(db.project, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)

    if form.accepted:
        # The update already happened!
        redirect(URL('index'))
    return dict(form=form) 

@action('delete_project/<project_id:int>')
@action.uses(db, session, auth.user)
def delete_project(project_id=None):
    assert project_id is not None
    # Check for correct permissions before editing
    if db.project[project_id] is None or not db.project[project_id].created_by == get_user():
        return HTTPStatus.BAD_REQUEST.name
    db(db.project.id == project_id).delete()
    redirect(URL('index'))