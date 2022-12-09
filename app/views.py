import logging, json
from flask import render_template, flash, redirect, Flask, request
from app import app, db, models, admin, login_manager
from flask_login import login_required, login_user, logout_user, current_user
from .forms import AddPost, AddComment, userLogin, createAccount, changePassword, changeName
from .models import User, Post, Comment, Like
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Like, db.session))

# Users will be asked to log in before viewing any other page
@app.route('/', methods=['GET', 'POST'])
def loginPage():
    # Form for login
    login = userLogin()

    if (login.validate_on_submit()):
        # Get the first user that is found with the inputted name
        user = models.User.query.filter_by(name=login.data["username"]).first()
        
        # If the user does not exist or they input the wrong password then flash error and redirect
        if (not user or not check_password_hash(user.password, login.data["password"])):
            flash('Please check your login details and try again.')
            return redirect('/')

        # Now we know the user is an existing user with correct details we can mark them as logged in
        # and redirect them to the home page
        login_user(user)
        return redirect('/home')

    return render_template('login.html', title="login", login=login)

# Users will be able to create an account should they not have one already
@app.route('/create_account', methods=['GET', 'POST'])
def createAccountPage():
    # Form for creating account
    create_acc = createAccount()

    if (create_acc.validate_on_submit()):
        # Search the db to see find if a user of the same name exists
        # If so flash error and redirect back to account creation
        existing = models.User.query.filter_by(name=create_acc.data["username"]).first()
        if(existing):
            flash('username taken')
            return redirect('/create_account')
        
        # Check that both password inputs match
        if(create_acc.data["password"] != create_acc.data["check_password"]):
            flash('Passwords do not match')
            return redirect('/create_account')

        # Add new user to the database
        addition = models.User(name=create_acc.data["username"],
                            password=generate_password_hash(create_acc.data["password"]),
                            email=create_acc.data["email"])
        db.session.add(addition)
        db.session.commit()

        # Redirect back to login after account creation
        return redirect('/')
    return render_template('create_account.html', title="Create Account", create_acc=create_acc)

# Remove login cookies and redirect back to login
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/user_settings', methods=["GET", "POST"])
@login_required
def user_settings():
    change_name = changeName()
    change_password = changePassword()

    if(change_name.validate_on_submit()):
        existing = models.User.query.filter_by(name=change_name.data["newName"]).first()

        if(existing):
            flash("Username taken")

            return redirect("/user_settings")

        if(not check_password_hash(current_user.password, change_name.data["password"])):
            flash("Incorrect password")

            return redirect("/user_settings")

        current_user.name = change_name.data["newName"]
        db.session.commit()

        return redirect("user_settings")


    if(change_password.validate_on_submit()):
        if(not check_password_hash(current_user.password, change_password.data["currentPassword"])):
            flash("Password incorrect")
            return redirect("/user_settings")

        if(change_password.data["newPassword"] != change_password.data["checkPassword"]):
            flash("New passwords do not match")

            return redirect("/user_settings")

        current_user.password=generate_password_hash(change_password.data["newPassword"])
        db.session.commit()
        
        return redirect("/user_settings")

    return render_template('edit_account.html', change_password=change_password, change_name = change_name)

# Home page which welcomes user and shows all their own posts
@app.route('/home')
@login_required
def home():
    # find all posts by the current user so they can be displayed
    user_id=current_user.id
    post = models.Post.query.filter_by(user_id=current_user.id)

    return render_template('home.html', title='home', post=post)

# Page to show all posts from newest to oldest
@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    posts = {'description': 'View posts from other users!'}
    # Get all posts and users from db
    post = models.Post.query.all()
    users = models.User.query.all()

    # Reverse posts list as we want to sort from biggest id to smallest
    post.reverse()

    return render_template('posts.html', title='posts', posts=posts, post=post, users=users)

# Page to add a post to the website
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    # Form for adding a post
    form = AddPost()

    if (form.validate_on_submit()):
        # Add post to db and redirect to the list of posts
        addition = models.Post(title=form.data["title"],body=form.data["body"],topic=form.data["tag"],user_id=current_user.id)
        db.session.add(addition)
        db.session.commit()

        return redirect("/posts")

    return render_template('add_post.html', title='add post', form=form)

# Pages created for each post in order to show comments and post body
@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    # Form to add comments
    add_comment = AddComment()

    # Get all users, current post and all comments for curent post
    users = models.User.query.all()
    post = models.Post.query.get(post_id)
    comments = models.Comment.query.filter_by(post_id=post_id)

    if (add_comment.validate_on_submit()):
        # Add comment to db and redirect back to current post
        addition = models.Comment(body=add_comment.data["body"], liked = 0,user_id=current_user.id,post_id=post_id)
        db.session.add(addition)
        db.session.commit()

        return redirect("/posts/" + str(post_id))


    return render_template('post.html', title=post.title, postID=post_id, comments = comments, post=post, users=users, add_comment=add_comment)

@app.route("/like", methods=['POST'])
def like_button():
    data = json.loads(request.data)
    comment_id = int(data.get("comment_id"))
    status = "Ok"
    amount = 1
    likes = models.Like.query.filter_by(comment_id=comment_id)

    for like in likes:
        print(like.comment_id)
        if(like.user_id == current_user.id):
            likeId = like.id
            status = "Not OK"
            amount = -1

    if(status == "Ok"):
        print("lol")
        addition = models.Like(user_id=current_user.id, comment_id=comment_id)
        db.session.add(addition)

        comment = models.Comment.query.get(comment_id)
        comment.liked = comment.liked + 1

        db.session.commit()
    
    else:
        print("lolmao")
        Like.query.filter_by(id=likeId).delete()

        comment = models.Comment.query.get(comment_id)
        comment.liked = comment.liked - 1

        db.session.commit()



    return json.dumps({'status': status, 'comment_id': comment_id, 'amount': amount})

