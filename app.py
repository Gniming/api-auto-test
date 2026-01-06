from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.env import Env
from app.models.test_case import TestCase
from app.routes.auth import hash_password

app = create_app()

# 创建初始用户
with app.app_context():
    # 检查是否已存在用户
    if User.query.count() == 0:
        # 创建管理员用户
        admin_user = User(
            username='admin',
            password_hash=hash_password('123456'),
            nickname='管理员'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("初始管理员用户已创建: admin/123456")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)