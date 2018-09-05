from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Uploaded_files
import boto3, botocore

import os

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login-example/database.db'
# bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))

# @LoginManager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class LoginForm(FlaskForm):
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
#     remember = BooleanField('remember me')

# class RegisterForm(FlaskForm):
#     email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

def upload_to_s3(file, bucket_name, acl='public-read'):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("S3 erros: ", e)
        return e

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
@login_required
def index():
    # imgs = current_user.get_images()
    # img_urls = []
    # for i in imgs:
    #     current_img_url = os.path.join(app.config['UPLOAD_FOLDER'], i.filename)
    #     img_urls.append(current_img_url)

    # return render_template('index.html', images=img_urls)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalide username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

        
        # if user:
        #     if check_password_hash(user.password, form.password.data):
        #         login_user(user, remember=form.remember.data)
        #         return redirect(url_for('dashboard'))

        # return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        # new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('New user has been created!')
        return redirect(url_for('login'))

        # return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image upload successful!')
            # user = User.query.filter_by(username=current_user.name).first()
            upload_image = Uploaded_files(filename=filename, author=current_user)
            db.session.add(upload_image)
            db.session.commit()
            return redirect(url_for('index'))
    return 'Unknown Errors'
            

if __name__ == '__main__':
    app.run(debug=True)
