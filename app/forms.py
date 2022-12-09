from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, IntegerField, EmailField
from wtforms.validators import DataRequired

# Form for adding a post
# Doesn't need user as we can get it from cookies
class AddPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Post Body', validators=[DataRequired()])
    tag = SelectField('tag', choices=[("None"), ("Rant"), ("Appreciation"), ("Suggestion"), ("Question")])

# Form for adding a comment
# Doesn't need user as we can get it from cookies
# Doesn't need post as we can get it from the current page
class AddComment(FlaskForm):
    body = StringField('Comment Body', validators=[DataRequired()])

# User authentication form
class userLogin(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Form for creating an account
class createAccount(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    check_password = PasswordField('Check Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])

# Form to allow user to change their password
class changePassword(FlaskForm):
    currentPassword = PasswordField('Password', validators=[DataRequired()])
    newPassword = PasswordField('New Password', validators=[DataRequired()])
    checkPassword = PasswordField('Check Password', validators = [DataRequired()])

class changeName(FlaskForm):
    newName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])