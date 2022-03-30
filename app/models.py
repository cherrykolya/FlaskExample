from . import db
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager


# MODELS

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    file_path = db.Column(db.String(20))
    
    posts = db.relationship('Post', back_populates="category")

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship('Post', back_populates="author")

    @property
    def password(self):
        raise AttributeError('Доступ к паролю запрещен')

    @password.setter
    def password(self, passwor):
        self.password_hash = generate_password_hash(passwor)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    header = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime())
    text = db.Column(db.String())
    photo = db.Column(db.String())
    
    author = db.relationship("User", back_populates="posts")
    category = db.relationship("Category", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    created_at = db.Column(db.DateTime())
    text = db.Column(db.String())

    author = db.relationship("User")
    post = db.relationship('Post', back_populates="comments")

@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)