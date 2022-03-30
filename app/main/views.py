from flask import render_template, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import select
from . import main
from .forms import NameForm, PostForm
from .utils import CategoriesEnum
from .. import db
from ..models import User, Post, Role
from datetime import datetime
import os


# VIEWS

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        #photo = form.photo.raw_data[0].stream._file
        d = os.path.abspath(os.getcwd()) + f'/app/static/{form.photo.data.filename}'
        
        with open(d,'wb') as out: ## Open temporary file as bytes
            out.write(form.photo.raw_data[0].stream._file.read())

        post = Post(author_id=int(session['_user_id']),
                    category_id = CategoriesEnum(form.category.data).to_value(),
                    header=form.header.data,
                    text=form.text.data,
                    created_at=datetime.now(),
                    photo= form.photo.data.filename)

        db.session.add(post)
        db.session.commit()
        return render_template('post_created.html') 
    return render_template('create_post.html', form=form)

@main.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = User.query.all()

    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts.html', phrase="Hi!", posts=posts)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
        form = form, name = session.get('name'),
        known = session.get('known', False))

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    #db.drop_all()
    #db.create_all()
    user_id = int(session['_user_id'])
    user = User.query.filter_by(id=user_id).first()
    return render_template('profile.html',name = session.get('name'),known = session.get('known', False), posts=user.posts)