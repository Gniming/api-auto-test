from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.env import Env
from app import db
from datetime import datetime

env = Blueprint('env', __name__)

@env.route('/api/envs', methods=['GET'])
@login_required
def get_envs():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        # 获取所有环境
        pagination = Env.query.paginate(page=page, per_page=page_size, error_out=False)
        
        # 格式化环境数据
        envs_data = []
        for e in pagination.items:
            envs_data.append({
                'id': e.id,
                'name': e.name,
                'base_url': e.base_url,
                'description': e.description,
                'creator_id': e.creator_id,
                'created_at': e.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': e.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'envs': envs_data,
                'pagination': {
                    'total': pagination.total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': pagination.pages
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取环境列表失败: {str(e)}'
        })

@env.route('/api/envs', methods=['POST'])
@login_required
def create_env():
    try:
        data = request.get_json()
        name = data.get('name')
        base_url = data.get('base_url')
        description = data.get('description')
        
        if not name or not base_url:
            return jsonify({
                'code': 400,
                'msg': '环境名称和基础 URL 不能为空'
            })
        
        # 创建新环境
        new_env = Env(
            name=name,
            base_url=base_url,
            description=description,
            creator_id=current_user.id
        )
        db.session.add(new_env)
        db.session.commit()
        
        # 返回创建的环境信息
        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': {
                'env': {
                    'id': new_env.id,
                    'name': new_env.name,
                    'base_url': new_env.base_url,
                    'description': new_env.description,
                    'creator_id': new_env.creator_id,
                    'created_at': new_env.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': new_env.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'创建环境失败: {str(e)}'
        })

@env.route('/api/envs/<int:env_id>', methods=['PUT'])
@login_required
def update_env(env_id):
    try:
        # 查找环境
        env = Env.query.filter_by(id=env_id).first()
        
        if not env:
            return jsonify({
                'code': 404,
                'msg': '环境不存在'
            })
        
        # 更新环境信息
        data = request.get_json()
        name = data.get('name')
        base_url = data.get('base_url')
        description = data.get('description')
        
        if not name or not base_url:
            return jsonify({
                'code': 400,
                'msg': '环境名称和基础 URL 不能为空'
            })
        
        env.name = name
        env.base_url = base_url
        env.description = description
        env.updated_at = datetime.now()
        db.session.commit()
        
        # 返回更新后的环境信息
        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': {
                'env': {
                    'id': env.id,
                    'name': env.name,
                    'base_url': env.base_url,
                    'description': env.description,
                    'creator_id': env.creator_id,
                    'created_at': env.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': env.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'更新环境失败: {str(e)}'
        })

@env.route('/api/envs/<int:env_id>', methods=['DELETE'])
@login_required
def delete_env(env_id):
    try:
        # 查找环境
        env = Env.query.filter_by(id=env_id).first()
        
        if not env:
            return jsonify({
                'code': 404,
                'msg': '环境不存在'
            })
        
        # 删除环境
        db.session.delete(env)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'删除环境失败: {str(e)}'
        })