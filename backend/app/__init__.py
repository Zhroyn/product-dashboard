import logging
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import create_engine, text

# 创建数据库对象
db = SQLAlchemy()

# 创建登录管理对象
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化爬虫
from .crawlers import JDCrawler, TBCrawler
jd_crawler = JDCrawler()
tb_crawler = TBCrawler()

def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object('config.Config')

    # 若数据库不存在，则创建数据库
    engine = create_engine(app.config['SQLALCHEMY_ENGINE_URI'])
    database_name = app.config['DBNAME']
    with engine.connect() as connection:
        connection.execute(text(f'CREATE DATABASE IF NOT EXISTS {database_name}'))

    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # 初始化登录管理对象
    login_manager.init_app(app)

    # 注册蓝图
    from .routes import register_blueprints
    register_blueprints(app)

    # 初始化 CSRF 保护
    csrf = CSRFProtect(app)

    return app
