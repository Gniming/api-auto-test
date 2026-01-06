from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime

auth = Blueprint('auth', __name__)

def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def hash_password(password):
    return pbkdf2_sha256.hash(password)

@auth.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'code': 400,
                'msg': '用户名和密码不能为空'
            })
        
        # 查询用户
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({
                'code': 401,
                'msg': '用户名或密码错误'
            })
        
        # 验证密码
        if not verify_password(password, user.password_hash):
            return jsonify({
                'code': 401,
                'msg': '用户名或密码错误'
            })
        
        # 更新最后登录时间
        user.last_login = datetime.now()
        db.session.commit()
        
        # 登录用户
        login_user(user)
        
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'登录失败: {str(e)}'
        })

@auth.route('/api/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({
            'code': 200,
            'msg': '注销成功'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'注销失败: {str(e)}'
        })