from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.common_params import CommonParams
from app import db
from datetime import datetime
import json

common_params = Blueprint('common_params', __name__)

@common_params.route('/api/common-params', methods=['GET'])
@login_required
def get_common_params():
    try:
        # 获取查询参数
        project_id = request.args.get('project_id', type=int)
        
        # 构建查询
        query = CommonParams.query
        
        # 如果指定了项目ID，则过滤
        if project_id is not None:
            query = query.filter_by(project_id=project_id)
        else:
            # 否则获取全局参数（project_id为null）和所有项目级参数
            query = query
        
        # 执行查询
        params_list = query.all()
        
        # 格式化数据
        params_data = []
        for params in params_list:
            params_data.append({
                'id': params.id,
                'project_id': params.project_id,
                'name': params.name,
                'headers': json.loads(params.headers),
                'description': params.description,
                'creator_id': params.creator_id,
                'created_at': params.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'common_params': params_data
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取公共参数组列表失败: {str(e)}'
        })

@common_params.route('/api/common-params', methods=['POST'])
@login_required
def create_common_params():
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        name = data.get('name')
        headers = data.get('headers')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'code': 400,
                'msg': '参数组名称不能为空'
            })
        
        if not headers:
            return jsonify({
                'code': 400,
                'msg': 'headers不能为空'
            })
        
        # 创建新公共参数组
        new_params = CommonParams(
            project_id=project_id,
            name=name,
            headers=json.dumps(headers),
            description=description,
            creator_id=current_user.id
        )
        db.session.add(new_params)
        db.session.commit()
        
        # 返回创建的参数组信息
        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': {
                'common_params': {
                    'id': new_params.id,
                    'project_id': new_params.project_id,
                    'name': new_params.name,
                    'headers': json.loads(new_params.headers),
                    'description': new_params.description,
                    'creator_id': new_params.creator_id,
                    'created_at': new_params.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'创建公共参数组失败: {str(e)}'
        })

@common_params.route('/api/common-params/<int:params_id>', methods=['PUT'])
@login_required
def update_common_params(params_id):
    try:
        # 查找公共参数组
        params = CommonParams.query.filter_by(id=params_id).first()
        
        if not params:
            return jsonify({
                'code': 404,
                'msg': '公共参数组不存在'
            })
        
        # 更新公共参数组信息
        data = request.get_json()
        project_id = data.get('project_id')
        name = data.get('name')
        headers = data.get('headers')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'code': 400,
                'msg': '参数组名称不能为空'
            })
        
        if not headers:
            return jsonify({
                'code': 400,
                'msg': 'headers不能为空'
            })
        
        params.project_id = project_id
        params.name = name
        params.headers = json.dumps(headers)
        params.description = description
        params.updated_at = datetime.now()
        db.session.commit()
        
        # 返回更新后的参数组信息
        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': {
                'common_params': {
                    'id': params.id,
                    'project_id': params.project_id,
                    'name': params.name,
                    'headers': json.loads(params.headers),
                    'description': params.description,
                    'creator_id': params.creator_id,
                    'created_at': params.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'更新公共参数组失败: {str(e)}'
        })

@common_params.route('/api/common-params/<int:params_id>', methods=['DELETE'])
@login_required
def delete_common_params(params_id):
    try:
        # 查找公共参数组
        params = CommonParams.query.filter_by(id=params_id).first()
        
        if not params:
            return jsonify({
                'code': 404,
                'msg': '公共参数组不存在'
            })
        
        # 删除公共参数组
        db.session.delete(params)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'删除公共参数组失败: {str(e)}'
        })