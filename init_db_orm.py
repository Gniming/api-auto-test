from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.env import Env
from app.models.test_case import TestCase
from app.models.case_step import CaseStep
from app.models.request_data import RequestData
from app.models.extract import Extract
from app.models.assert_rule import AssertRule
from app.models.common_params import CommonParams
from app.models.task import Task

app = create_app()

with app.app_context():
    # 创建所有表
    db.create_all()
    print("数据库表结构已创建")
    
    # 检查是否已存在用户
    if User.query.count() == 0:
        # 创建管理员用户
        from app.routes.auth import hash_password
        admin_user = User(
            username='admin',
            password_hash=hash_password('123456'),
            nickname='管理员'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("初始管理员用户已创建: admin/123456")