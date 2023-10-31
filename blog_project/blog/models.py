from blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
Creating a User class to make an instance of a user with attributes such as:
    Attribute:
    id: a unique ID for each user
    username: A unique username for each user of the blog
    email:
    password:
    posts:

"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = relationship('Comment', backref='user',
                            lazy=True, primaryjoin='User.id ==Comment.user_id')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.username})'


"""
A class for Post:
    Attribute:
    id: A unique identifier.
    title: Title for the post.
    date: The date it was posted.
    content: content of the post.
    user_id:
"""


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.title})'


"""
A class for comment.
"""


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp())

    def __init__(self, post_id, user_id, content):
        """
        initializing comment attribite as part of a post.
        """
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
