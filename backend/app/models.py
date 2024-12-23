from datetime import datetime, timezone
from enum import Enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


def utcnow():
    return datetime.now(timezone.utc)


class Source(Enum):
    JD = "京东"
    TB = "淘宝"


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String(50), primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    shop_name = db.Column(db.String(100), nullable=False)
    shop_url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    extra_info = db.Column(db.JSON, nullable=False)
    source = db.Column(db.Enum(Source), nullable=False)

    price_histories = db.relationship('PriceHistory', backref='product')

    def __repr__(self):
        return f"<Product {self.id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'price': self.price,
            'shop_name': self.shop_name,
            'shop_url': self.shop_url,
            'image_url': self.image_url,
            'extra_info': self.extra_info,
            'source': self.source.value
        }

    @staticmethod
    def from_dict(data):
        return Product(
            id=data['id'],
            url=data['url'],
            title=data['title'],
            price=data['price'],
            shop_name=data['shop_name'],
            shop_url=data['shop_url'],
            image_url=data['image_url'],
            extra_info=data['extra_info'],
            source=Source(data['source'])
        )


class PriceHistory(db.Model):
    __tablename__ = 'price_history'

    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=utcnow, nullable=False)

    def __repr__(self):
        return f'<PriceHistory {self.product_id} - {self.timestamp}>'


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)
    cookies = db.Column(db.JSON, default={source.value: [] for source in Source}, nullable=False)

    price_alerts = db.relationship('PriceAlert', backref='user')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login_at = utcnow()
        db.session.commit()


class PriceAlert(db.Model):
    __tablename__ = 'price_alert'

    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(50), db.ForeignKey('product.id'), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def __repr__(self):
        return f'<PriceAlert {self.user_id} - {self.product_id} - {self.target_price}>'

    def to_dict(self):
        return {
            'target_price': self.target_price,
            'created_at': self.created_at,
            **Product.query.get(self.product_id).to_dict()
        }
