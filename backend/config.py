import os

class Config:
    DEBUG = False
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

    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_ENGINE_URI = f"{DIALCT}+{DRITVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    SQLALCHEMY_DATABASE_URI = f"{SQLALCHEMY_ENGINE_URI}/{DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    MAIL_SERVER = 'smtp.zju.edu.cn'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '3220103230@zju.edu.cn'
    MAIL_PASSWORD = 'GPngGpRKuhWARs7s'
    MAIL_DEFAULT_SENDER = ('商品比价网站', '3220103230@zju.edu.cn')