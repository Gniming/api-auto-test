# API 自动测试平台

一个基于 Python Flask 开发的 API 自动测试平台，支持测试用例管理、环境配置、批量执行测试和详细的执行报告。

## 功能特性

- **用户认证**：基于 Session 的登录认证
- **项目管理**：创建、编辑、删除项目
- **环境管理**：配置全局测试环境
- **测试用例管理**：
  - 基本的 CRUD 操作
  - 批量保存测试步骤和配置
  - 支持变量提取和断言验证
- **测试执行**：
  - 调试执行（指定步骤）
  - 完整测试用例执行
  - 详细的执行报告
- **内置函数**：支持随机数据生成等内置函数
- **公共参数**：支持全局和项目级公共参数

## 技术栈

- **后端**：Python 3.8+, Flask 2.0.1
- **数据库**：MySQL
- **ORM**：SQLAlchemy
- **认证**：Flask-Login
- **密码加密**：passlib
- **HTTP 客户端**：requests
- **前端**：（预留接口，可配合任意前端框架使用）

## 快速开始

### 1. 环境准备

- Python 3.8+
- MySQL 5.7+
- pip 包管理工具

### 2. 安装依赖

```bash
# 克隆项目（如果有）
git clone <项目地址>
cd api-auto-test

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 数据库配置

1. **创建数据库**：
   在 MySQL 中创建一个新的数据库，例如 `api_auto_test`。

2. **配置环境变量**：
   在项目根目录创建 `.env` 文件，配置数据库连接信息：

   ```dotenv
   # .env
   DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/api_auto_test
   SECRET_KEY=your_secret_key_here
   ```

   其中：
   - `root`：MySQL 用户名
   - `123456`：MySQL 密码
   - `localhost:3306`：MySQL 地址和端口
   - `api_auto_test`：数据库名称

### 4. 初始化数据库

```bash
# 运行数据库初始化脚本
python init_db_orm.py
```

这将：
- 创建所有必要的数据库表
- 创建初始管理员用户（用户名：admin，密码：123456）

### 5. 启动应用

```bash
# 启动 Flask 应用
python app.py
```

应用将运行在 `http://localhost:5001`。

## API 接口文档

### 1. 用户认证

#### POST /api/login
- **描述**：用户登录
- **请求参数**：
  ```json
  {
    "username": "admin",
    "password": "123456"
  }
  ```
- **成功返回**：
  ```json
  {
    "code": 200,
    "msg": "登录成功",
    "data": {
      "user": {
        "id": 1,
        "username": "admin",
        "nickname": "管理员",
        "last_login": "2026-01-06 10:00:00"
      }
    }
  }
  ```

#### POST /api/logout
- **描述**：用户登出
- **请求参数**：无
- **成功返回**：
  ```json
  {
    "code": 200,
    "msg": "注销成功"
  }
  ```

### 2. 项目管理

#### GET /api/projects
- **描述**：获取所有项目列表
- **成功返回**：项目列表

#### POST /api/projects
- **描述**：创建新项目
- **请求参数**：
  ```json
  {
    "name": "测试项目",
    "description": "项目描述"
  }
  ```

#### PUT /api/projects/<id>
- **描述**：更新项目信息
- **请求参数**：同创建

#### DELETE /api/projects/<id>
- **描述**：删除项目
- **成功返回**：
  ```json
  {
    "code": 200,
    "msg": "删除成功"
  }
  ```

### 3. 环境管理

#### GET /api/envs
- **描述**：获取所有环境列表
- **成功返回**：环境列表

#### POST /api/envs
- **描述**：创建新环境
- **请求参数**：
  ```json
  {
    "name": "测试环境",
    "base_url": "http://test.api.example.com",
    "description": "测试环境描述"
  }
  ```

#### PUT /api/envs/<id>
- **描述**：更新环境信息
- **请求参数**：同创建

#### DELETE /api/envs/<id>
- **描述**：删除环境
- **成功返回**：
  ```json
  {
    "code": 200,
    "msg": "删除成功"
  }
  ```

### 4. 测试用例管理

#### GET /api/projects/<project_id>/cases
- **描述**：获取指定项目下的测试用例列表

#### POST /api/projects/<project_id>/cases
- **描述**：创建新测试用例
- **请求参数**：
  ```json
  {
    "name": "测试用例",
    "description": "用例描述"
  }
  ```

#### PUT /api/cases/<id>
- **描述**：更新测试用例信息
- **请求参数**：同创建

#### DELETE /api/cases/<id>
- **描述**：删除测试用例
- **成功返回**：
  ```json
  {
    "code": 200,
    "msg": "删除成功"
  }
  ```

#### GET /api/cases/<case_id>/edit
- **描述**：获取测试用例完整信息（用于编辑）
- **成功返回**：包含用例基本信息和所有步骤的详细信息

#### PUT /api/cases/<case_id>/steps/batch
- **描述**：批量保存测试用例步骤和配置
- **请求参数**：
  ```json
  {
    "case_name": "测试用例名称",
    "steps": [
      {
        "id": 1, // 有 id 表示更新，无 id 表示新增
        "name": "步骤名称",
        "method": "GET",
        "path": "/api/endpoint",
        "sort": 10,
        "enabled": true,
        "request": {
          "headers": {"Content-Type": "application/json"},
          "params": {},
          "data": {},
          "timeout": 30
        },
        "extracts": [
          {"id": 1, "var_name": "variable", "expression": "$.data.id"}
        ],
        "asserts": [
          {"id": 1, "assert_type": "status_code", "expect_value": "200"}
        ]
      }
    ]
  }
  ```

### 5. 测试执行

#### POST /api/debug/run
- **描述**：调试执行指定步骤
- **请求参数**：
  ```json
  {
    "env_id": 1,
    "step_ids": [1, 2, 3],
    "common_params_ids": [1, 2]
  }
  ```

#### POST /api/cases/<case_id>/run
- **描述**：执行完整测试用例
- **请求参数**：
  ```json
  {
    "env_id": 1,
    "common_params_ids": [1, 2]
  }
  ```

#### GET /api/tasks/<task_id>
- **描述**：查看单次执行报告详情
- **成功返回**：包含执行摘要和详细日志

#### GET /api/projects/<project_id>/reports
- **描述**：获取项目下最近执行报告列表
- **成功返回**：项目下最近的执行报告列表

### 6. 公共参数管理

#### GET /api/common-params
- **描述**：获取公共参数组列表
- **查询参数**：
  - `project_id`：可选，过滤项目级参数

#### POST /api/common-params
- **描述**：创建公共参数组
- **请求参数**：
  ```json
  {
    "project_id": null, // null 表示全局参数
    "name": "全局参数",
    "headers": {"Content-Type": "application/json"},
    "description": "参数描述"
  }
  ```

#### PUT /api/common-params/<id>
- **描述**：更新公共参数组
- **请求参数**：同创建

#### DELETE /api/common-params/<id>
- **描述**：删除公共参数组
- **成功返回**：
  ```json
  {
    "code": 200,
    "msg": "删除成功"
  }
  ```

## 内置函数

平台支持以下内置函数，可在测试用例中使用：

- `${__random_plate()}`：生成随机车牌，如 `京A12345`
- `${__random_phone()}`：生成随机手机号，如 `13812345678`
- `${__random_string(10)}`：生成指定长度的随机字符串
- `${__random_int(100, 999)}`：生成指定范围的随机整数
- `${__timestamp()}`：生成当前时间戳
- `${__date('%Y-%m-%d')}`：生成指定格式的当前日期
- `${__uuid()}`：生成 UUID

## 项目结构

```
api-auto-test/
├── app/
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── project.py    # 项目模型
│   │   ├── env.py        # 环境模型
│   │   ├── test_case.py  # 测试用例模型
│   │   ├── case_step.py  # 测试步骤模型
│   │   ├── request_data.py # 请求数据模型
│   │   ├── extract.py    # 变量提取模型
│   │   ├── assert_rule.py # 断言规则模型
│   │   ├── common_params.py # 公共参数模型
│   │   └── task.py       # 执行任务模型
│   ├── routes/           # 路由
│   │   ├── auth.py       # 认证路由
│   │   ├── project.py    # 项目路由
│   │   ├── env.py        # 环境路由
│   │   ├── test_case.py  # 测试用例路由
│   │   ├── common_params.py # 公共参数路由
│   │   └── execution.py  # 执行路由
│   ├── utils/            # 工具函数
│   │   └── execution.py  # 执行相关工具
│   ├── __init__.py       # 应用初始化
│   └── config.py         # 配置文件
├── venv/                 # 虚拟环境
├── .env                  # 环境变量
├── app.py                # 应用入口
├── init_db_orm.py        # 数据库初始化
├── requirements.txt      # 依赖文件
└── README.md             # 项目说明
```

## 数据库表结构

项目包含以下数据库表：

1. **user**：用户表
2. **project**：项目表
3. **env**：环境表
4. **test_case**：测试用例表
5. **case_step**：测试步骤表
6. **request_data**：请求数据表
7. **extract**：变量提取表
8. **assert_rule**：断言规则表
9. **common_params**：公共参数表
10. **task**：执行任务表

详细的表结构可参考 `app/models/` 目录下的模型定义。

## 常见问题

### 1. 数据库连接失败

- 检查 `.env` 文件中的数据库连接信息是否正确
- 确保 MySQL 服务正在运行
- 确保数据库用户有足够的权限

### 2. 内置函数不生效

- 确保函数调用格式正确，如 `${__random_string(10)}`
- 检查函数参数是否正确传递

### 3. 执行测试失败

- 检查环境配置是否正确（特别是 base_url）
- 检查测试步骤的路径和方法是否正确
- 查看执行报告中的详细错误信息

## 扩展建议

1. **前端开发**：使用 Vue.js、React 等前端框架开发友好的 UI 界面
2. **定时任务**：添加定时执行测试的功能
3. **测试套件**：支持将多个测试用例组合成测试套件
4. **数据驱动**：支持从 Excel、CSV 等文件读取测试数据
5. **CI/CD 集成**：提供与 CI/CD 工具的集成接口

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系项目维护者。