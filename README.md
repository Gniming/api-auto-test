# API 自动化测试平台

## 项目概述

这是一个 API 自动化测试平台，支持以下功能：
- 项目管理
- 环境配置管理
- 测试用例管理（支持步骤编辑、变量提取、断言规则）
- 公共参数管理
- 执行报告管理
- 步骤顺序调整（支持拖拽排序和上下移动）

## 技术栈

### 后端
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- MySQL

### 前端
- Vue 3
- Element Plus
- Axios
- Vue Router

## 部署步骤

### 1. 克隆项目

```bash
git clone <仓库地址>
cd api-auto-test
```

### 2. 后端部署

#### 2.1 创建虚拟环境
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 2.2 安装依赖
```bash
pip install -r requirements.txt
```

#### 2.3 配置数据库
- 修改 `app/config.py` 文件中的数据库配置
- 创建数据库表结构
```bash
python app.py db migrate
python app.py db upgrade
```

#### 2.4 启动后端服务
```bash
# 开发模式
python app.py runserver

# 生产模式
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### 3. 前端部署

#### 3.1 安装依赖
```bash
cd frontend
npm install
```

#### 3.2 构建项目
```bash
npm run build
```

#### 3.3 部署前端静态文件
- 将 `frontend/dist` 目录下的文件部署到 Nginx 或其他静态文件服务器
- 配置 Nginx 反向代理到后端服务

### 4. 环境变量配置

#### 后端环境变量
- `FLASK_ENV`: 运行环境 (development/production)
- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: Flask 密钥

#### 前端环境变量
- 修改 `frontend/.env` 文件中的 API 地址配置

## 启动项目

### 开发模式

#### 后端
```bash
source venv/bin/activate  # 激活虚拟环境
python app.py runserver
```

#### 前端
```bash
cd frontend
npm run dev
```

### 生产模式

#### 后端
```bash
source venv/bin/activate  # 激活虚拟环境
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

#### 前端
```bash
cd frontend
npm run build
# 将 dist 目录部署到 Nginx
```

## 基础功能

### 1. 项目管理
- 创建、编辑、删除项目
- 查看项目列表（支持分页）

### 2. 环境管理
- 创建、编辑、删除环境配置
- 配置环境 base_url
- 查看环境列表（支持分页）

### 3. 测试用例管理
- 创建、编辑、删除测试用例
- 编辑用例步骤（支持添加、修改、删除步骤）
- 步骤详情配置（请求方法、路径、参数、头部、Body）
- 变量提取规则配置
- 断言规则配置
- 步骤顺序调整（支持拖拽排序和上下移动）
- 查看用例列表（支持分页）

### 4. 公共参数管理
- 创建、编辑、删除公共参数
- 查看公共参数列表（支持分页）

### 5. 执行报告管理
- 查看执行报告列表（支持分页）
- 查看报告详情

## API 接口

### 项目相关
- `GET /api/projects`: 获取项目列表（支持分页）
- `POST /api/projects`: 创建项目
- `PUT /api/projects/{id}`: 更新项目
- `DELETE /api/projects/{id}`: 删除项目

### 环境相关
- `GET /api/envs`: 获取环境列表（支持分页）
- `POST /api/envs`: 创建环境
- `PUT /api/envs/{id}`: 更新环境
- `DELETE /api/envs/{id}`: 删除环境

### 测试用例相关
- `GET /api/projects/{id}/cases`: 获取项目用例列表（支持分页）
- `POST /api/projects/{id}/cases`: 创建测试用例
- `GET /api/cases/{id}/edit`: 获取用例编辑信息
- `PUT /api/cases/{id}/steps/batch`: 批量更新用例步骤
- `POST /api/cases/{id}/run`: 执行测试用例

### 公共参数相关
- `GET /api/common-params`: 获取公共参数列表（支持分页）
- `POST /api/common-params`: 创建公共参数
- `PUT /api/common-params/{id}`: 更新公共参数
- `DELETE /api/common-params/{id}`: 删除公共参数

### 执行报告相关
- `GET /api/projects/{id}/reports`: 获取项目报告列表（支持分页）
- `GET /api/reports/{id}`: 获取报告详情

## 注意事项

1. 首次部署时需要创建数据库表结构
2. 确保后端服务和前端服务的地址配置正确
