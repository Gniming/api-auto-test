from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.test_case import TestCase
from app.models.case_step import CaseStep
from app.models.request_data import RequestData
from app.models.extract import Extract
from app.models.assert_rule import AssertRule
from app import db
from datetime import datetime
import json

test_case = Blueprint('test_case', __name__)

@test_case.route('/api/projects/<int:project_id>/cases', methods=['GET'])
@login_required
def get_cases(project_id):
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        # 获取指定项目下的所有测试用例
        pagination = TestCase.query.filter_by(project_id=project_id).order_by(TestCase.sort).paginate(page=page, per_page=page_size, error_out=False)
        
        # 格式化测试用例数据
        cases_data = []
        from app.models.user import User
        for case in pagination.items:
            # 获取创建人昵称
            creator_nickname = ''
            creator = User.query.filter_by(id=case.creator_id).first()
            if creator:
                creator_nickname = creator.nickname or creator.username
            
            cases_data.append({
                'id': case.id,
                'name': case.name,
                'description': case.description,
                'sort': case.sort,
                'creator_id': case.creator_id,
                'creator_name': creator_nickname,
                'created_at': case.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': case.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'cases': cases_data,
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
            'msg': f'获取测试用例列表失败: {str(e)}'
        })

@test_case.route('/api/projects/<int:project_id>/cases', methods=['POST'])
@login_required
def create_case(project_id):
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'code': 400,
                'msg': '测试用例名称不能为空'
            })
        
        # 创建新测试用例
        new_case = TestCase(
            project_id=project_id,
            name=name,
            description=description,
            sort=0,
            creator_id=current_user.id
        )
        db.session.add(new_case)
        db.session.commit()
        
        # 返回创建的测试用例信息
        return jsonify({
            'code': 200,
            'msg': '创建成功',
            'data': {
                'case': {
                    'id': new_case.id,
                    'name': new_case.name,
                    'description': new_case.description,
                    'sort': new_case.sort,
                    'creator_id': new_case.creator_id,
                    'created_at': new_case.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': new_case.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'创建测试用例失败: {str(e)}'
        })

@test_case.route('/api/cases/<int:case_id>', methods=['PUT'])
@login_required
def update_case(case_id):
    try:
        # 查找测试用例
        case = TestCase.query.filter_by(id=case_id).first()
        
        if not case:
            return jsonify({
                'code': 404,
                'msg': '测试用例不存在'
            })
        
        # 更新测试用例信息
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            return jsonify({
                'code': 400,
                'msg': '测试用例名称不能为空'
            })
        
        case.name = name
        case.description = description
        case.updated_at = datetime.now()
        db.session.commit()
        
        # 返回更新后的测试用例信息
        return jsonify({
            'code': 200,
            'msg': '更新成功',
            'data': {
                'case': {
                    'id': case.id,
                    'name': case.name,
                    'description': case.description,
                    'sort': case.sort,
                    'creator_id': case.creator_id,
                    'created_at': case.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': case.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'更新测试用例失败: {str(e)}'
        })

@test_case.route('/api/cases/<int:case_id>', methods=['DELETE'])
@login_required
def delete_case(case_id):
    try:
        # 查找测试用例
        case = TestCase.query.filter_by(id=case_id).first()
        
        if not case:
            return jsonify({
                'code': 404,
                'msg': '测试用例不存在'
            })
        
        # 删除测试用例
        db.session.delete(case)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'删除测试用例失败: {str(e)}'
        })

@test_case.route('/api/cases/<int:case_id>/edit', methods=['GET'])
@login_required
def get_case_edit_info(case_id):
    try:
        # 查找测试用例
        case = TestCase.query.filter_by(id=case_id).first()
        
        if not case:
            return jsonify({
                'code': 404,
                'msg': '测试用例不存在'
            })
        
        # 查找测试用例的所有步骤
        steps = CaseStep.query.filter_by(case_id=case_id).order_by(CaseStep.sort).all()
        
        # 格式化测试用例数据
        case_data = {
            'id': case.id,
            'name': case.name,
            'description': case.description
        }
        
        # 格式化步骤数据
        steps_data = []
        for step in steps:
            # 查找步骤的请求数据
            request_data = RequestData.query.filter_by(step_id=step.id).first()
            
            # 查找步骤的变量提取
            extracts = Extract.query.filter_by(step_id=step.id).all()
            
            # 查找步骤的断言规则
            asserts = AssertRule.query.filter_by(step_id=step.id).all()
            
            # 格式化请求数据
            request_info = {}
            if request_data:
                request_info = {
                    'headers': json.loads(request_data.headers) if request_data.headers else {},
                    'params': json.loads(request_data.params) if request_data.params else {},
                    'data': json.loads(request_data.data) if request_data.data else {},
                    'timeout': request_data.timeout
                }
            
            # 格式化变量提取
            extracts_info = []
            for extract in extracts:
                extracts_info.append({
                    'id': extract.id,
                    'var_name': extract.var_name,
                    'expression': extract.expression
                })
            
            # 格式化断言规则
            asserts_info = []
            for assert_rule in asserts:
                asserts_info.append({
                    'id': assert_rule.id,
                    'assert_type': assert_rule.assert_type,
                    'expect_value': assert_rule.expect_value,
                    'actual_source': assert_rule.actual_source
                })
            
            # 构建步骤信息
            step_info = {
                'id': step.id,
                'name': step.name,
                'method': step.method,
                'path': step.path,
                'sort': step.sort,
                'enabled': step.enabled,
                'request': request_info,
                'extracts': extracts_info,
                'asserts': asserts_info
            }
            
            steps_data.append(step_info)
        
        return jsonify({
            'code': 200,
            'data': {
                'case': case_data,
                'steps': steps_data
            }
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取测试用例详情失败: {str(e)}'
        })

@test_case.route('/api/cases/<int:case_id>/steps/batch', methods=['PUT'])
@login_required
def batch_save_steps(case_id):
    try:
        # 查找测试用例
        case = TestCase.query.filter_by(id=case_id).first()
        
        if not case:
            return jsonify({
                'code': 404,
                'msg': '测试用例不存在'
            })
        
        # 获取请求数据
        data = request.get_json()
        case_name = data.get('case_name')
        steps = data.get('steps', [])
        
        # 更新测试用例名称和描述
        if case_name:
            case.name = case_name
        case_description = data.get('case_description')
        if case_description is not None:
            case.description = case_description
        case.updated_at = datetime.now()
        
        # 获取原用例下所有 step_id、request_data_id、extract_ids、assert_ids
        old_steps = CaseStep.query.filter_by(case_id=case_id).all()
        old_step_ids = [step.id for step in old_steps]
        
        # 存储所有旧的相关 ID
        old_request_data_ids = []
        old_extract_ids = []
        old_assert_ids = []
        
        for step in old_steps:
            # 获取请求数据 ID
            request_data = RequestData.query.filter_by(step_id=step.id).first()
            if request_data:
                old_request_data_ids.append(request_data.id)
            
            # 获取变量提取 ID
            extracts = Extract.query.filter_by(step_id=step.id).all()
            old_extract_ids.extend([extract.id for extract in extracts])
            
            # 获取断言规则 ID
            asserts = AssertRule.query.filter_by(step_id=step.id).all()
            old_assert_ids.extend([assert_rule.id for assert_rule in asserts])
        
        # 处理前端传来的步骤
        new_step_ids = []
        
        for step_data in steps:
            step_id = step_data.get('id')
            name = step_data.get('name')
            method = step_data.get('method')
            path = step_data.get('path')
            sort = step_data.get('sort', 0)
            enabled = step_data.get('enabled', True)
            request_info = step_data.get('request', {})
            extracts_info = step_data.get('extracts', [])
            asserts_info = step_data.get('asserts', [])
            
            if step_id:
                # 更新现有步骤
                step = CaseStep.query.filter_by(id=step_id).first()
                if step:
                    step.name = name
                    step.method = method
                    step.path = path
                    step.sort = sort
                    step.enabled = enabled
                    step.updated_at = datetime.now()
                    new_step_ids.append(step_id)
                    
                    # 更新或创建请求数据
                    request_data = RequestData.query.filter_by(step_id=step_id).first()
                    if not request_data:
                        request_data = RequestData(
                            step_id=step_id,
                            creator_id=current_user.id
                        )
                        db.session.add(request_data)
                    
                    # 更新请求数据
                    request_data.headers = json.dumps(request_info.get('headers', {}))
                    request_data.params = json.dumps(request_info.get('params', {}))
                    request_data.data = json.dumps(request_info.get('data', {}))
                    request_data.timeout = request_info.get('timeout', 30)
                    request_data.updated_at = datetime.now()
                    
                    # 处理变量提取
                    existing_extracts = Extract.query.filter_by(step_id=step_id).all()
                    existing_extract_ids = {extract.id: extract for extract in existing_extracts}
                    
                    for extract_info in extracts_info:
                        extract_id = extract_info.get('id')
                        var_name = extract_info.get('var_name')
                        expression = extract_info.get('expression')
                        
                        if extract_id and extract_id in existing_extract_ids:
                            # 更新现有变量提取
                            extract = existing_extract_ids[extract_id]
                            extract.var_name = var_name
                            extract.expression = expression
                            extract.updated_at = datetime.now()
                            del existing_extract_ids[extract_id]
                        else:
                            # 创建新变量提取
                            new_extract = Extract(
                                step_id=step_id,
                                var_name=var_name,
                                expression=expression,
                                creator_id=current_user.id
                            )
                            db.session.add(new_extract)
                    
                    # 删除未更新的变量提取
                    for extract_id in existing_extract_ids:
                        extract = existing_extract_ids[extract_id]
                        db.session.delete(extract)
                    
                    # 处理断言规则
                    existing_asserts = AssertRule.query.filter_by(step_id=step_id).all()
                    existing_assert_ids = {assert_rule.id: assert_rule for assert_rule in existing_asserts}
                    
                    for assert_info in asserts_info:
                        assert_id = assert_info.get('id')
                        assert_type = assert_info.get('assert_type')
                        expect_value = assert_info.get('expect_value')
                        actual_source = assert_info.get('actual_source', 'response_body')
                        
                        if assert_id and assert_id in existing_assert_ids:
                            # 更新现有断言规则
                            assert_rule = existing_assert_ids[assert_id]
                            assert_rule.assert_type = assert_type
                            assert_rule.expect_value = expect_value
                            assert_rule.actual_source = actual_source
                            assert_rule.updated_at = datetime.now()
                            del existing_assert_ids[assert_id]
                        else:
                            # 创建新断言规则
                            new_assert = AssertRule(
                                step_id=step_id,
                                assert_type=assert_type,
                                expect_value=expect_value,
                                actual_source=actual_source,
                                creator_id=current_user.id
                            )
                            db.session.add(new_assert)
                    
                    # 删除未更新的断言规则
                    for assert_id in existing_assert_ids:
                        assert_rule = existing_assert_ids[assert_id]
                        db.session.delete(assert_rule)
            else:
                # 创建新步骤
                new_step = CaseStep(
                    case_id=case_id,
                    name=name,
                    method=method,
                    path=path,
                    sort=sort,
                    enabled=enabled,
                    creator_id=current_user.id
                )
                db.session.add(new_step)
                db.session.flush()  # 获取新步骤的 ID
                new_step_ids.append(new_step.id)
                
                # 创建请求数据
                new_request_data = RequestData(
                    step_id=new_step.id,
                    headers=json.dumps(request_info.get('headers', {})),
                    params=json.dumps(request_info.get('params', {})),
                    data=json.dumps(request_info.get('data', {})),
                    timeout=request_info.get('timeout', 30),
                    creator_id=current_user.id
                )
                db.session.add(new_request_data)
                
                # 创建变量提取
                for extract_info in extracts_info:
                    var_name = extract_info.get('var_name')
                    expression = extract_info.get('expression')
                    
                    new_extract = Extract(
                        step_id=new_step.id,
                        var_name=var_name,
                        expression=expression,
                        creator_id=current_user.id
                    )
                    db.session.add(new_extract)
                
                # 创建断言规则
                for assert_info in asserts_info:
                    assert_type = assert_info.get('assert_type')
                    expect_value = assert_info.get('expect_value')
                    actual_source = assert_info.get('actual_source', 'response_body')
                    
                    new_assert = AssertRule(
                        step_id=new_step.id,
                        assert_type=assert_type,
                        expect_value=expect_value,
                        actual_source=actual_source,
                        creator_id=current_user.id
                    )
                    db.session.add(new_assert)
        
        # 找出被删除的步骤
        deleted_step_ids = [step_id for step_id in old_step_ids if step_id not in new_step_ids]
        
        # 删除被删除的步骤及其相关数据
        for step_id in deleted_step_ids:
            # 删除请求数据
            request_data = RequestData.query.filter_by(step_id=step_id).first()
            if request_data:
                db.session.delete(request_data)
            
            # 删除变量提取
            extracts = Extract.query.filter_by(step_id=step_id).all()
            for extract in extracts:
                db.session.delete(extract)
            
            # 删除断言规则
            asserts = AssertRule.query.filter_by(step_id=step_id).all()
            for assert_rule in asserts:
                db.session.delete(assert_rule)
            
            # 删除步骤
            step = CaseStep.query.filter_by(id=step_id).first()
            if step:
                db.session.delete(step)
        
        # 提交所有更改
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'msg': '保存成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'msg': f'保存失败: {str(e)}'
        })