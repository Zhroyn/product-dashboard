import os

class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = False

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