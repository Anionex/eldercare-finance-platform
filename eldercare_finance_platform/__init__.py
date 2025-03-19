import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化数据库
db = SQLAlchemy()

# 初始化登录管理器
login_manager = LoginManager()

def create_app():
    # 创建Flask应用
    app = Flask(__name__, instance_relative_config=True)
    
    # 配置应用
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', secrets.token_hex(16)),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'eldercare.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY'),
        OPENAI_API_BASE=os.environ.get('OPENAI_API_BASE')
    )
    
    # 确保instance文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化登录管理器
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    
    # 添加user_loader回调函数
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 注册蓝图
    from . import auth, main, chat
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(chat.bp)
    
    return app
