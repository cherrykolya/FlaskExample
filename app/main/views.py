from flask import render_template, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import select
from PIL import Image
from . import main
from .forms import NameForm, PostForm, CommentForm
from .utils import CategoriesEnum
from .. import db
from ..models import User, Post, Category, Comment
from datetime import datetime
import os


# VIEWS

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        #photo = form.photo.raw_data[0].stream._file
        user = User.query.filter_by(id=int(session['_user_id'])).first()
        d = os.path.abspath(os.getcwd()) + f'/app/static/{user.username}/{form.photo.data.filename}'
        
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


@main.route('/posts/<category>', methods=['GET', 'POST'])
def posts(category):
    if category == 'all':
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('posts.html', posts=posts)
    else:
        category = Category.query.filter_by(id=int(category)).first()
        #posts = User.query.all()
        #posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('posts.html', posts=category.posts)

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
@login_required
def profile():
    #db.drop_all()
    #db.create_all()
    user_id = int(session['_user_id'])
    user = User.query.filter_by(id=user_id).first()
    return render_template('profile.html',name = session.get('name'),known = session.get('known', False), posts=user.posts, user=user)

@main.route('/conversation/<post_id>', methods=['GET', 'POST'])
@login_required
def conversation(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(author_id=int(session['_user_id']),
            post_id= int(post_id),
            text=form.text.data,
            created_at=datetime.now())
        db.session.add(comment)
        db.session.commit()
        post = Post.query.filter_by(id=int(post_id)).first() 
        return render_template('conversation.html', posts=post, form=form) 
    post = Post.query.filter_by(id=int(post_id)).first()
    return render_template('conversation.html', posts=post, form=form)