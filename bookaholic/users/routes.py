from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, logout_user, current_user, login_user
from bookaholic import db,bcrypt
from bookaholic.models import User, Post
from bookaholic.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,ResetPassword, ResetForm
from bookaholic.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)

@users.route("/login", methods = ['GET', 'POST'])
def login():
    #if user is logged in using the current_user method from flask_login
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        #check dataabase hashedpassword with the user form password
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, form.remember.data)
            # if the user type from url  ,then capture that value after next and go to that url after the user logged in
            next_page = request.args.get('next')
            flash("You have logged in succesfully",'success')
            return redirect (next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Your username or password is incorrect ','danger')
    return  render_template('login.html', form = form, title='login')

@users.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #stores values in user dv
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data} successfully",'success')
        return redirect(url_for('users.login'))

    return  render_template('register.html', form=form,title='register')

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data  
        db.session.commit()
        flash ('your account has been updated','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile_pics/' + current_user.image)
    return  render_template('account.html',title='account', image_file = image_file, form = form)

@users.route("/user/<string:username>", methods = ['GET', 'POST'])
def user_posts(username):
    page = request.args.get('page', 1 ,type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date.desc())\
        .paginate( page = page, per_page = 5)
    return render_template("user_posts.html", title = 'posts', posts= posts, user = user)

@users.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return render_template(url_for('main.index'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been send to reset your password')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title = 'Reset Password', form = form)

@users.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return render_template(url_for('main.index'))
    form = ResetForm()
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid Token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        #stores values in user dv
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f"Account password updated successfully",'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',form = form)
