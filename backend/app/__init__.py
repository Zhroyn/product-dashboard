import logging
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

# 初始化数据库
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

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
    app.config.from_pyfile('../config.py')

    # 若数据库不存在，则创建数据库
    engine = create_engine(app.config['SQLALCHEMY_ENGINE_URI'])
    database_name = app.config['DBNAME']
    with engine.connect() as connection:
        connection.execute(text(f'CREATE DATABASE IF NOT EXISTS {database_name}'))

    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    # 注册蓝图
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
