from flask import render_template,redirect,url_for, request, abort, flash, Blueprint
from flask_login import login_required, current_user
from bookaholic import db
from bookaholic.models import Post
from bookaholic.posts.forms import PostForm

pos = Blueprint('posts',__name__)


@pos.route("/posts")
def posts():
    page = request.args.get('page', 1 ,type = int)
    posts = Post.query.order_by(Post.date.desc()).paginate( page = page, per_page = 5)
    return render_template("posts.html", title = 'posts', posts= posts)

@pos.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('posts.posts'))
    return render_template('create_post.html', title = 'New_Post',form = form,legend = 'New Post' )

@pos.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post, post = post)

@pos.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
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

@pos.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted','success')
    return redirect(url_for('posts.posts'))


