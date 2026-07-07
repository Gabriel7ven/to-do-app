from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from todolist.auth import login_required
# from todolist.db import get_db
from todolist import db
from todolist.models.models import User, Note

bp = Blueprint('notes', __name__)

@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))

    stmt = (
        db.select(Note, User.username)
        .join(User, Note.author_id == User.id)
        .where(Note.author_id == g.user.id)
        .order_by(Note.created.desc())
    )

    tasks = db.session.execute(stmt).all()
    # db = get_db()
    # tasks = db.execute(
    #     'SELECT p.id, title, task, created, author_id, username'
    #     ' FROM note p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.author_id = ?'
    #     ' ORDER BY created DESC', (g.user['id'],)
    # ).fetchall()
    return render_template('notes/index.html', tasks=tasks)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        task = request.form['task']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO note (title, task, author_id)'
                ' VALUES (?, ?, ?)',
                (title, task, g.user['id'])
            )
            db.commit()
            return redirect(url_for('notes.index'))

    return render_template('notes/create.html')

def get_task(id, check_author=True):
    task = get_db().execute(
        'SELECT p.id, title, task, created, author_id, username'
        ' FROM note p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    if check_author and task['author_id'] != g.user['id']:
        abort(403)

    return task


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        title = request.form['title']
        task_text = request.form['task']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE note SET title = ?, task = ?'
                ' WHERE id = ?',
                (title, task_text, id)
            )
            db.commit()
            return redirect(url_for('notes.index'))

    return render_template('notes/update.html', task=task)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM note WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('notes.index'))