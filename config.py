#CSRF key for my website so that it is more secure
WTF_CSRF_ENABLED = True

SECRET_KEY = 'abs15wathha_forumapp'

import os

# Set up for SQLalchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True  