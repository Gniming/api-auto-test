from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.project import Project
from app import db
from datetime import datetime

project = Blueprint('project', __name__)

@project.route('/api/projects', methods=['GET'])
@login_required
def get_projects():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        # 获取当前用户的所有项目
        print(f"Current user ID: {current_user.id}")
        pagination = Project.query.paginate(page=page, per_page=page_size, error_out=False)
        
        # 格式化项目数据
        projects_data = []
        for proj in pagination.items:
            print(f"Project ID: {proj.id}, Creator ID: {proj.creator_id}")
            projects_data.append({
                'id': proj.id,
                'name': proj.name,
                'description': proj.description,
                'creator_id': proj.creator_id,
                'created_at': proj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': proj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'projects': projects_data,
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
            'msg': f'获取项目列表失败: {str(e)}'
        })

@project.route('/api/projects', methods=['POST'])
@login_required
def create_project():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'code': 400,
                'msg': '项目名称不能为空'
            })
        
        # 创建新项目
        print(f"Creating project for user ID: {current_user.id}")
        new_project = Project(
            name=name,
            description=description,
            creator_id=current_user.id
        )
        db.session.add(new_project)
        db.session.commit()
        
        # 返回创建的项目信息
        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': {
                'project': {
                    'id': new_project.id,
                    'name': new_project.name,
                    'description': new_project.description,
                    'creator_id': new_project.creator_id,
                    'created_at': new_project.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': new_project.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'创建项目失败: {str(e)}'
        })

@project.route('/api/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    try:
        # 查找项目
        print(f"Updating project {project_id} for user ID: {current_user.id}")
        project = Project.query.filter_by(id=project_id).first()
        
        if not project:
            return jsonify({
                'code': 404,
                'msg': '项目不存在'
            })
        
        # 更新项目信息
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'code': 400,
                'msg': '项目名称不能为空'
            })
        
        project.name = name
        project.description = description
        project.updated_at = datetime.now()
        db.session.commit()
        
        # 返回更新后的项目信息
        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': {
                'project': {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'creator_id': project.creator_id,
                    'created_at': project.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': project.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'更新项目失败: {str(e)}'
        })

@project.route('/api/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    try:
        # 查找项目
        print(f"Deleting project {project_id} for user ID: {current_user.id}")
        project = Project.query.filter_by(id=project_id).first()
        
        if not project:
            return jsonify({
                'code': 404,
                'msg': '项目不存在'
            })
        
        # 删除项目
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'删除项目失败: {str(e)}'
        })