import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def init_database():
    # 从环境变量中获取数据库连接信息
    db_uri = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456@localhost/api_auto_test'
    print(f"Using database URL: {db_uri}")
    
    # 解析数据库连接字符串
    import re
    match = re.match(r'mysql\+pymysql://(.*?):(.*?)@(.*?)/(.*)', db_uri)
    if not match:
        print("Invalid database URL format")
        return
    
    user, password, host_port, db_name = match.groups()
    # 分离主机名和端口
    if ':' in host_port:
        host, port = host_port.split(':')
    else:
        host = host_port
        port = 3306
    # 去除可能的查询参数
    db_name = db_name.split('?')[0]
    print(f"Database config: user={user}, host={host}, port={port}, db={db_name}")
    
    try:
        # 连接到 MySQL 服务器
        print("Attempting to connect to MySQL server...")
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            charset='utf8mb4'
        )
        print("Connected to MySQL server successfully")
        
        try:
            with conn.cursor() as cursor:
                # 创建数据库（如果不存在）
                print(f"Creating database {db_name} if not exists...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"Database {db_name} created successfully")
                
                # 选择数据库
                conn.select_db(db_name)
                print(f"Selected database {db_name}")
                
                # 执行创建表的 SQL 语句
                print("Creating tables...")
                sql_statements = """
                -- 1. 环境表（全局） 
                CREATE TABLE IF NOT EXISTS env ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(50) NOT NULL UNIQUE, 
                    base_url VARCHAR(255) NOT NULL, 
                    description VARCHAR(255), 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 2. 项目表 
                CREATE TABLE IF NOT EXISTS project ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(100) NOT NULL, 
                    description TEXT, 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 3. 测试用例表 
                CREATE TABLE IF NOT EXISTS test_case ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    project_id INT NOT NULL, 
                    name VARCHAR(200) NOT NULL, 
                    description TEXT, 
                    sort INT DEFAULT 0, 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 4. 用例步骤表（核心：集成 method + path） 
                CREATE TABLE IF NOT EXISTS case_step ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    case_id INT NOT NULL, 
                    step_type ENUM('request','wait','script') NOT NULL DEFAULT 'request', 
                    name VARCHAR(200), 
                    method ENUM('GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS') DEFAULT 'GET', 
                    path VARCHAR(500), 
                    sort INT DEFAULT 0, 
                    enabled TINYINT(1) DEFAULT 1, 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 5. 请求数据表 
                CREATE TABLE IF NOT EXISTS request_data ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    step_id INT NOT NULL, 
                    headers LONGTEXT, 
                    params LONGTEXT, 
                    data LONGTEXT, 
                    files LONGTEXT, 
                    timeout INT DEFAULT 30, 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 6. 变量提取表 
                CREATE TABLE IF NOT EXISTS extract ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    step_id INT NOT NULL, 
                    var_name VARCHAR(100) NOT NULL, 
                    expression TEXT NOT NULL, 
                    scope ENUM('case','global') DEFAULT 'case', 
                    var_type ENUM('string','int','bool','float') DEFAULT 'string',
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 7. 断言规则表 
                CREATE TABLE IF NOT EXISTS assert_rule ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    step_id INT NOT NULL, 
                    assert_type ENUM('status_code','contain','not_contain','json_equal','json_schema','regex','length','database') NOT NULL, 
                    expect_value LONGTEXT, 
                    actual_source VARCHAR(255)DEFAULT 'response_status', 
                    description VARCHAR(255), 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                ); 
                
                -- 8. 执行任务及报告表 
                CREATE TABLE IF NOT EXISTS task ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    project_id INT NOT NULL, 
                    case_id INT, 
                    env_id INT NOT NULL, 
                    name VARCHAR(200) NOT NULL, 
                    creator_id INT, 
                    status ENUM('pending','running','success','failed','stopped') DEFAULT 'pending', 
                    start_time DATETIME, 
                    end_time DATETIME, 
                    duration INT, 
                    pass_count INT DEFAULT 0, 
                    fail_count INT DEFAULT 0, 
                    total_steps INT DEFAULT 0, 
                    log LONGTEXT,  -- JSON 存储详细执行日志 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
                ); 
                
                -- 9. 公共参数表（新增，全局或项目级公共 headers，如 token） 
                CREATE TABLE IF NOT EXISTS common_params ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    project_id INT COMMENT '所属项目ID（NULL 表示全局公共参数）', 
                    name VARCHAR(100) NOT NULL COMMENT '参数组名称，如 "登录Token" 或 "全局Header"', 
                    headers LONGTEXT NOT NULL COMMENT '公共 headers JSON，例如 {"Authorization": "Bearer ${token}"}', 
                    description VARCHAR(255), 
                    creator_id INT, 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                    UNIQUE KEY uniq_project_name (project_id, name) 
                ); 
                
                -- 10. 用户表（极简） 
                CREATE TABLE IF NOT EXISTS user ( 
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    username VARCHAR(50) NOT NULL UNIQUE, 
                    password_hash VARCHAR(255) NOT NULL, 
                    nickname VARCHAR(50), 
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                    last_login DATETIME 
                );
                """
                
                # 分割 SQL 语句并执行
                tables_created = 0
                for statement in sql_statements.split(';'):
                    statement = statement.strip()
                    if statement and 'CREATE TABLE' in statement:
                        try:
                            cursor.execute(statement)
                            # 提取表名
                            table_name = re.search(r'CREATE TABLE IF NOT EXISTS (\w+)', statement).group(1)
                            print(f"Created table: {table_name}")
                            tables_created += 1
                        except Exception as e:
                            print(f"Error creating table: {e}")
                
                # 提交事务
                conn.commit()
                print(f"All tables created successfully! Total tables: {tables_created}")
                
        except Exception as e:
            print(f"Error creating tables: {e}")
            conn.rollback()
        finally:
            conn.close()
            print("Database connection closed")
            
    except Exception as e:
        print(f"Error connecting to MySQL server: {e}")
        print("Please check if MySQL server is running and the connection details are correct")

if __name__ == "__main__":
    init_database()