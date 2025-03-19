# 养老金融服务平台

## 项目简介

养老金融服务平台是一个专为老年人设计的金融咨询服务系统，主打养老金融咨询业务。平台利用微调的大模型与老年人进行智能交互，提供产品推荐、常识科普、个性化建议、财务评估、趋势分析、风险分析、风险管理、投资组合调整和方案制定等服务。

整体采用老年人喜欢的严肃正式配色，让人信服。平台具有大气的主页设计，滚动时有动画效果和背景切换，为用户提供良好的视觉体验。

## 功能特点

- **用户认证**：通过手机号和验证码进行简单登录
- **AI聊天界面**：
  - Google风格的初始搜索框
  - 平滑过渡到ChatGPT风格的聊天界面
  - 左侧历史对话抽屉
  - 不同颜色的消息气泡
  - Markdown和LaTeX渲染支持
  - 停止生成、重新生成功能
  - 消息编辑功能
  - 文件上传功能（支持文本类型）
- **功能模块**：
  - 虚拟人对话（开发中）
  - 咨询服务（产品推荐、常识科普、个性化建议等）
  - 财务分析（财务评估、趋势分析、风险分析等）
  - 投资管理（风险管理、调整投资组合、方案制定等）

## 技术栈

- **后端**：Flask
- **数据库**：SQLite
- **前端样式**：Tailwind CSS
- **AI对话**：OpenAI API

## 安装指南

### 环境要求

- Python 3.10+
- Node.js 14+
- npm 6+

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/Anionex/eldercare-finance-platform.git
cd eldercare-finance-platform
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
npm install
```

4. 构建CSS文件
```bash
npm run build-css
```

5. 配置环境变量
创建`.env`文件，添加以下内容：
```
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

6. 初始化数据库
```bash
python init_db.py
```

7. 启动应用
```bash
python app.py
```

8. 访问应用
浏览器打开 `http://localhost:5000`

## 部署指南

详细的部署指南请参考 [deployment_guide.md](deployment_guide.md)。

## 项目结构

```
eldercare_finance_platform/
├── app.py                      # 应用入口
├── init_db.py                  # 数据库初始化脚本
├── eldercare_finance_platform/ # 主应用包
│   ├── __init__.py             # 应用初始化
│   ├── auth.py                 # 认证模块
│   ├── chat.py                 # 聊天功能
│   ├── main.py                 # 主要路由
│   ├── models.py               # 数据模型
│   ├── static/                 # 静态资源
│   │   ├── css/                # CSS样式
│   │   │   ├── input.css       # TailwindCSS输入文件
│   │   │   ├── output.css      # TailwindCSS生成的输出文件
│   │   │   └── main.css        # 主要样式文件
│   │   ├── js/                 # JavaScript脚本
│   │   └── images/             # 图片资源
│   └── templates/              # HTML模板
│       ├── auth/               # 认证相关模板
│       ├── chat/               # 聊天相关模板
│       └── main/               # 主要页面模板
├── instance/                   # 实例文件夹（包含数据库）
├── node_modules/               # Node.js依赖
├── package.json                # npm配置
├── tailwind.config.js          # Tailwind配置
└── postcss.config.js           # PostCSS配置
```

## TailwindCSS配置说明

本项目使用TailwindCSS进行样式管理。为确保样式正确加载，请注意以下几点：

1. **正确的路径配置**：tailwind.config.js中的content路径必须指向正确的模板和JavaScript文件位置，即：
```js
content: [
  "./eldercare_finance_platform/templates/**/*.html",
  "./eldercare_finance_platform/static/**/*.js"
]
```

2. **依赖版本**：确保使用兼容的依赖版本，特别是：
```json
"devDependencies": {
  "autoprefixer": "^10.4.14",
  "postcss": "^8.4.24",
  "tailwindcss": "^3.3.2"
}
```

3. **CSS构建流程**：项目需要构建TailwindCSS才能正确显示样式，使用以下命令：
```bash
npm run build-css
```

4. **CSS文件结构**：
   - input.css：包含TailwindCSS指令
   - output.css：由TailwindCSS生成的最终CSS文件
   - main.css：项目自定义样式

## 使用说明

1. 注册/登录：使用手机号和验证码登录（当前版本验证码验证已设置为全部通过）
2. 主页：浏览平台介绍和功能
3. 聊天界面：在中央输入框输入问题，开始与AI助手对话
4. 功能入口：点击相应功能入口，体验不同服务（部分功能正在开发中）

## 开发计划

- [x] 环境设置
- [x] 数据库设计
- [x] 前端设计
- [x] 用户认证
- [x] AI聊天功能
- [x] 功能入口占位
- [x] 部署文档
- [x] 部署上线
- [x] 聊天界面增强
- [ ] 虚拟人（多模态数字人）实现
- [ ] 专业金融模型集成
- [ ] 移动端适配优化

## 常见问题解决

### 样式不显示问题

如果遇到样式不正确显示的问题，可能是由以下原因导致：

1. **TailwindCSS配置路径错误**：检查tailwind.config.js中的content路径是否正确指向eldercare_finance_platform目录下的templates和static文件夹。

2. **未构建CSS文件**：确保运行了`npm run build-css`命令生成output.css文件。

3. **依赖版本问题**：确保使用正确版本的TailwindCSS（v3.x）和相关依赖。

4. **CSS文件引用错误**：检查HTML模板中是否正确引用了output.css文件。

### 解决方法

1. 修改tailwind.config.js中的content路径：
```js
content: [
  "./eldercare_finance_platform/templates/**/*.html",
  "./eldercare_finance_platform/static/**/*.js"
]
```

2. 更新package.json中的依赖版本：
```json
"devDependencies": {
  "autoprefixer": "^10.4.14",
  "postcss": "^8.4.24",
  "tailwindcss": "^3.3.2"
}
```

3. 添加CSS构建脚本到package.json：
```json
"scripts": {
  "build-css": "npx tailwindcss -i ./eldercare_finance_platform/static/css/input.css -o ./eldercare_finance_platform/static/css/output.css --minify",
  "watch-css": "npx tailwindcss -i ./eldercare_finance_platform/static/css/input.css -o ./eldercare_finance_platform/static/css/output.css --watch"
}
```

4. 创建input.css文件并运行构建命令：
```bash
npm run build-css
```

## 贡献指南

欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 项目维护者：Anionex
- GitHub：[https://github.com/Anionex](https://github.com/Anionex)
