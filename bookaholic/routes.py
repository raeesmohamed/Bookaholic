import secrets
import os
from PIL import Image
from flask import render_template, url_for,flash,redirect,request,abort
from bookaholic import app,db,bcrypt
from bookaholic.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from bookaholic.models import User, Post
from flask_login import login_user, current_user,logout_user, login_required


@app.route("/")
@app.route("/index")
def index():
    # form = ReviewForm
    # if form.validate_on_submit:
    #     form.reviews.data 
    #     redirect(url_for('reviews'))
    return render_template("index.html", title = 'home', posts= posts)

@app.route("/posts")
def posts():
    # form = ReviewForm
    # if form.validate_on_submit:
    #     form.reviews.data 
    #     redirect(url_for('reviews'))
    posts = Post.query.all()
    return render_template("posts.html", title = 'posts', posts= posts)
# @app.route("/reviews", methods= ['POST'])
# def reviews():
#         jsonfile = 
#         review = db.execute('')
#         return render_template("reviews.html", title = 'reviews')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if user is logged in using the current_user method from flask_login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        #check dataabase hashedpassword with the user form password
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, form.remember.data)
            # if the user type from url  ,then capture that value after next and go to that url after the user logged in
            next_page = request.args.get('next')
            flash("You have logged in succesfully",'success')
            return redirect (next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Your username or password is incorrect ','danger')
    return  render_template('login.html', form = form, title='login')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #stores values in user dv
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data} successfully",'success')
        return redirect(url_for('login'))

    return  render_template('register.html', form=form,title='register')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(picture_form):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_form.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output = (125,125)
    i = Image.open(picture_form)
    i.thumbnail(output)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods = ['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile_pics/' + current_user.image)
    return  render_template('account.html',title='account', image_file = image_file, form = form)

@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('posts'))
    return render_template('create_post.html', title = 'New_Post',form = form,legend = 'New Post' )

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post, post = post)

@app.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash ('Your post has been updated', 'success')
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update_post',form = form, legend = 'Update Post')

@app.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted','success')
    return redirect(url_for('posts'))