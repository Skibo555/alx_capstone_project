from flask import render_template, redirect, url_for, flash, request, abort
from blog import app, db, bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, SearchForm
from .models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required
from .forms import CommentForm
#from flask import Blueprint

#blueprint = Blueprint('blueprint', __name__)

# Route to the homepage.


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('homepage.html', posts=posts)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data,
                              user_id=current_user.id, post_id=post.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
        return redirect(url_for('detail', post_id=post.id))
    return render_template('detail.html', post=post, comments=comments, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        flash('You registered successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('you already logged in', 'info')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('you logged in successfully', 'info')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('email or password is wrong', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out successfully', 'info')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        db.session.commit()
        flash('Update successfully', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('profile.html', form=form)


@app.route('/post/', methods=['GET'])
def display_posts():
    # retrive all posts from the database.
    posts = Post.query.all()
    return '<h1> Coming soon </h1>'


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.title.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('post created')
        return redirect(url_for('profile'))
    return render_template('new_post.html', form=form)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted, but why delete?', 'success')
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('post updated', 'success')
        return redirect(url_for('detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('update.html', form=form)


@app.route('/post/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        posts = Post.query.filter(
            Post.title.like(f"%{form.query.data}%")).all()
        if posts:
            return render_template('search.html', posts=posts, form=form)
        else:
            flash('No such post has been found!', 'danger')
            return render_template('search.html', form=form)
    return render_template('search.html', form=form)

# for the seaech bar to get search results displayed on the search bar.


@app.route('/search', methods=['GET'])
def search_post():
    query = request.args.get('query')
    search_results = Post.query.filter(Post.title.like(f"%{query}%")).all()
    return render_template('search_results.html', query=query, results=search_results)


@app.route('/marketplace/', methods=['GET'])
def marketplace():
    return '<h1> This is gonna be an exiting part of our project, <strong>Watch out </strong> <h1>'


@app.route('/farmerscorner/', methods=['GET'])
def farmerscorner():
    return '<h1> This is gonna be an exiting part of our project, <strong>Still struggling with the concept and how to present it</strong> <h1>'


@app.route('/about/', methods=['GET'])
def about():
    return render_template('aboutpage.html')


@app.route('/contact/', methods=['GET'])
def contact():
    return render_template('contact-us.html')


@app.route('/submit', methods=['POST'])
def form_submission():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(name, email, message)
    return "Form data recieved: Name - {}, Email - {}, Message - {}".format(name, email, message)
