from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from todolist.auth import login_required
from todolist import db
from todolist.models.models import User, Note

bp = Blueprint('notes', __name__)

@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))

    stmt = (
        db.select(Note)
        .join(User, Note.author_id == User.id)
        .where(Note.author_id == g.user.id)
        #.order_by(Note.created.desc())
    )

    tasks = db.session.execute(stmt).scalars()
    
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
            new_note = Note(title=title, task=task, author_id=g.user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('notes.index'))

    return render_template('notes/create.html')

def get_task(id, check_author=True):
    stmt = (
        db.select(Note)
        .join(User, Note.author_id == User.id)
        .where(Note.id == id)
    )

    task = db.session.execute(stmt).scalar_one_or_none()
    
    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    if check_author and task.author_id != g.user.id:
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
            task.title = title
            task.task = task_text
            db.session.commit()
            return redirect(url_for('notes.index'))

    return render_template('notes/update.html', task=task)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    task = get_task(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('notes.index'))