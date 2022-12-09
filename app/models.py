from app import db
from flask_login import UserMixin

# Table to hold user information with UserMixin to allow for login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

# Table to hold information about specific posts with a foreign key to the user that posted it
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    topic = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '{}{}{}'.format(self.title, self.topic, self.user)

# Table to hold information about Comments with foreign keys to the post it's attached to and the user that posted it
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    liked = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    likes = db.relationship('Like', backref='comment', lazy='dynamic')

    def __repr__(self):
        return 'userID={} \n postID={}'.format(self.user_id, self.post_id)

# Table to hold what user has liked what post so that they cannot like 1 comment more than once
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))