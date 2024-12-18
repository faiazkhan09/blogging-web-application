import os
import secrets
from PIL import Image
from flaskpro import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, Blueprint, request, abort
from flaskpro.form import SignupForm, LoginForm, AccountUpdateForm, PostForm
from flaskpro.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required




@app.route("/")
@app.route("/home")
def home():  
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.time_posted.desc()).paginate(page=page, per_page=2)
    return render_template("home.html", posts=posts)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = (
        SignupForm()
    )  
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)  
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for { form.username.data }!", "success"
        )  
        return redirect(url_for("login"))
    return render_template(
        "signup.html", title="Signup", form=form
    )  


@app.route("/login", methods=["GET", "POST"])
def login():
    if (
        current_user.is_authenticated
    ):  
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  
        if user and bcrypt.check_password_hash(user.password, form.password.data):  
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next") 
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(f"Incorrect Email or Password! Please check email and password!","danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))



def update_pic(form_pic): 
    rand_hex = secrets.token_hex(8) 
    file_name, file_extention = os.path.splitext(form_pic.filename) 
    pic_name = rand_hex + file_extention
    pic_path = os.path.join(app.root_path, 'static/Pictures', pic_name)

    output_size = (125,125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)

    prev_picture = os.path.join(app.root_path, 'static/Pictures', current_user.image_file) 
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return pic_name

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = update_pic(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your information has been updated!','success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="Pictures/" + current_user.image_file)
    return render_template("account.html", title=current_user.username, image_file=image_file, form=form)
          

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():    
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) 
        db.session.add(post)
        db.session.commit()
        flash('Post has been created', 'success')
        return redirect(url_for('home'))    
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': 
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))    
