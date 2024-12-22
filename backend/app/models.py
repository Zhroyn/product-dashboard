from datetime import datetime, timezone
from enum import Enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


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


def get_utc_now():
    return datetime.now(timezone.utc)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

    # 设置密码时，使用 bcrypt 加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码是否正确
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 更新最后登录时间
    def update_last_login(self):
        self.last_login_at = get_utc_now()
