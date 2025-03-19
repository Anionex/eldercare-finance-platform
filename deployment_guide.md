# 养老金融服务平台部署文档

## 环境要求

### 系统要求
- 操作系统：Linux (Ubuntu 20.04+)、macOS 或 Windows
- Python 3.8+
- Node.js 14+
- npm 6+

### 依赖包
- Flask 3.0+
- Flask-SQLAlchemy 3.0+
- Flask-Login 0.6+
- python-dotenv 1.0+
- OpenAI 1.0+
- Tailwind CSS

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/your-username/eldercare_finance_platform.git
cd eldercare_finance_platform
```

### 2. 创建并激活虚拟环境（可选但推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. 安装Python依赖

```bash
pip install flask flask-sqlalchemy flask-login python-dotenv openai
```

### 4. 安装Node.js依赖

```bash
npm install
```

### 5. 配置环境变量

创建一个`.env`文件在项目根目录下，添加以下内容：

```
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1  # 如果使用自定义API基础URL，请修改此项
```

注意：请将`your_secret_key_here`替换为一个随机生成的密钥，将`your_openai_api_key_here`替换为您的OpenAI API密钥。

### 6. 初始化数据库

```bash
python init_db.py
```

## 配置说明

### 数据库配置

默认情况下，应用使用SQLite数据库，存储在`instance/eldercare.sqlite`文件中。如果需要使用其他数据库（如MySQL或PostgreSQL），请修改`eldercare_finance_platform/__init__.py`文件中的`SQLALCHEMY_DATABASE_URI`配置。

### OpenAI API配置

应用使用OpenAI API进行AI聊天功能。请确保在`.env`文件中正确配置了`OPENAI_API_KEY`和`OPENAI_API_BASE`。

## 启动指南

### 开发环境启动

```bash
python app.py
```

应用将在`http://localhost:5000`上运行。

### 生产环境部署

#### 使用Gunicorn（推荐用于Linux/macOS）

1. 安装Gunicorn

```bash
pip install gunicorn
```

2. 启动应用

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "eldercare_finance_platform:create_app()"
```

#### 使用Waitress（适用于Windows）

1. 安装Waitress

```bash
pip install waitress
```

2. 创建`wsgi.py`文件

```python
from eldercare_finance_platform import create_app

app = create_app()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
```

3. 启动应用

```bash
python wsgi.py
```

## Nginx配置（可选，用于生产环境）

如果您希望使用Nginx作为反向代理，可以使用以下配置：

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 部署到公网

### 方法1：使用云服务器

1. 在云服务提供商（如AWS、阿里云、腾讯云等）购买一台服务器
2. 按照上述步骤在服务器上部署应用
3. 配置域名解析到服务器IP
4. 配置SSL证书（推荐使用Let's Encrypt）

### 方法2：使用PaaS平台

#### Heroku部署

1. 安装Heroku CLI并登录

```bash
npm install -g heroku
heroku login
```

2. 创建Heroku应用

```bash
heroku create eldercare-finance-platform
```

3. 添加Procfile文件

```
web: gunicorn "eldercare_finance_platform:create_app()"
```

4. 配置环境变量

```bash
heroku config:set SECRET_KEY=your_secret_key_here
heroku config:set OPENAI_API_KEY=your_openai_api_key_here
heroku config:set OPENAI_API_BASE=https://api.openai.com/v1
```

5. 部署应用

```bash
git push heroku main
```

#### 使用Vercel部署

1. 安装Vercel CLI并登录

```bash
npm install -g vercel
vercel login
```

2. 创建`vercel.json`文件

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

3. 部署应用

```bash
vercel
```

## 故障排除

### 常见问题

1. **数据库初始化失败**
   - 确保`instance`目录存在且有写入权限
   - 检查数据库连接字符串是否正确

2. **OpenAI API调用失败**
   - 验证API密钥是否正确
   - 检查网络连接是否正常
   - 确认API基础URL是否正确

3. **静态文件无法加载**
   - 确保`static`目录中的文件存在
   - 检查Nginx配置是否正确处理静态文件

### 日志查看

应用日志默认输出到控制台。在生产环境中，建议配置日志文件：

```python
import logging
from logging.handlers import RotatingFileHandler

# 在create_app函数中添加
if not app.debug:
    file_handler = RotatingFileHandler('logs/eldercare.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Eldercare Finance Platform startup')
```

## 安全建议

1. 在生产环境中使用强密码作为`SECRET_KEY`
2. 定期更新依赖包以修复安全漏洞
3. 使用HTTPS加密传输数据
4. 不要在代码中硬编码敏感信息，使用环境变量
5. 定期备份数据库
