from . import db
from enum import Enum


class Source(Enum):
    JD = "京东"
    TB = "淘宝"


class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    shop_name = db.Column(db.String(100), nullable=False)
    shop_url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    extra_info = db.Column(db.JSON, nullable=False)
    source = db.Column(db.Enum(Source), nullable=False)

    def __repr__(self):
        return f"<Product {self.id}>"


class Cookie(db.Model):
    source = db.Column(db.Enum(Source), primary_key=True)
    cookies = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Cookie {self.source.value}>"
