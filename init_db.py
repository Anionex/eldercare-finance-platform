import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from eldercare_finance_platform import create_app, db
from eldercare_finance_platform.models import User, ChatHistory

app = create_app()

# 创建应用上下文
with app.app_context():
    # 创建所有数据库表
    db.create_all()
    
    print("数据库初始化完成！")
