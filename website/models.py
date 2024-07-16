from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', backref='search', cascade="all, delete, delete-orphan")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    searches = db.relationship('Search')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    price = db.Column(db.String(50))
    image = db.Column(db.String(255))
    rating = db.Column(db.String(10))
    ratings_number = db.Column(db.String(10))
    description = db.Column(db.String(1000000))
    availability = db.Column(db.String(255))
    prime = db.Column(db.String(255))
    discount = db.Column(db.String(255))
    seller = db.Column(db.String(255))
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'))

class AutomatedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    price = db.Column(db.String(50))
    image = db.Column(db.String(255))
    rating = db.Column(db.String(10))
    ratings_number = db.Column(db.String(10))
    description = db.Column(db.String(1000000))
    availability = db.Column(db.String(255))
    prime = db.Column(db.String(255))
    discount = db.Column(db.String(255))
    seller = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
