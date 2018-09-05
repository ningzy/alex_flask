from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    images = db.relationship('Uploaded_files', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_images(self):
        imgs = Uploaded_files.query.filter_by(username=self.username)
        return imgs.order_by(Uploaded_files.timestamp.desc())

class Uploaded_files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('user.username'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    filename = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Images {}>'.format(self.filename)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))