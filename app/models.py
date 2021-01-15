from datetime import datetime as dt
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=dt.utcnow)
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='author', lazy='dynamic')

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return f'User[{self.username}, {self.email}]'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(20), nullable=False)
    images = db.relationship('ProductImage', backref='images', lazy='dynamic')
    name = db.Column(db.String(64), unique=False,  nullable=False)
    count = db.Column(db.Integer,  nullable=False)
    price = db.Column(db.Float, nullable=False)
    description=db.Column(db.String(200),  nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    category = db.Column(db.String(60), nullable=False)
    color= db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='ordersProduct', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}, {self.count}'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    count = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(60), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status=db.Column(db.String(15), default='ordered')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), default='None')





    def __repr__(self):
        return f'{self.name}, {self.count}'


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(64), nullable=False)
    last_name=db.Column(db.String(64), nullable=False)
    phone =db.Column (db.Integer, nullable=False)
    district = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    mail = db.Column(db.String(25), nullable=False)
    number = db.Column (db.Integer, nullable=False)
    orders = db.relationship('Order', backref='orderAddress', lazy='dynamic')


    def __repr__(self):
        return f'{self.district}, {self.region}'

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')


