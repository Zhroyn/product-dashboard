import os

class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = False
    SCHEDULER_API_ENABLED = True

    DIALCT = "mysql"
    DRITVER = "pymysql"
    HOST = '127.0.0.1'
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = "123456"
    DBNAME = 'flask_app_db'

    SQLALCHEMY_ENGINE_URI = f"{DIALCT}+{DRITVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    SQLALCHEMY_DATABASE_URI = f"{SQLALCHEMY_ENGINE_URI}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'hr.zheng.zju@gmail.com'
    MAIL_PASSWORD = 'jmbs acgd vgiq foiy'
    MAIL_DEFAULT_SENDER = ('商品比价网站', 'hr.zheng.zju@gmail.com')