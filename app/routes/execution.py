from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.env import Env
from app.models.case_step import CaseStep
from app.models.test_case import TestCase
from app.models.common_params import CommonParams
from app.models.project import Project
from app.models.task import Task
from app import db
from datetime import datetime
import json
from app.utils.execution import execute_single_step, resolve_variables

execution = Blueprint('execution', __name__)

def run_steps(env_id, step_ids, common_params_ids=None, case_id=None):
    """
    执行测试步骤的公共函数
    env_id：环境 ID
    step_ids：步骤 ID 列表
    common_params_ids：公共参数组 ID 列表
    case_id：测试用例 ID（可选）
    返回执行结果
    """
    try:
        # 验证环境是否存在
        env = Env.query.filter_by(id=env_id).first()
        if not env:
            return {'code': 404, 'msg': '环境不存在'}
        
        env_base_url = env.base_url
        
        # 验证所有步骤是否存在
        steps = CaseStep.query.filter(CaseStep.id.in_(step_ids)).all()
        if len(steps) != len(step_ids):
            return {'code': 404, 'msg': '部分步骤不存在'}
        
        # 加载公共参数
        common_headers_list = []
        if common_params_ids:
            common_params = CommonParams.query.filter(CommonParams.id.in_(common_params_ids)).all()
            for params in common_params:
                try:
                    headers = json.loads(params.headers)
                    common_headers_list.append(headers)
                except:
                    pass
        
        # 初始化全局 headers
        global_headers = {}
        # 对公共 headers 进行变量替换（仅内置函数）
        from app.utils.execution import BUILTIN_FUNCTIONS
        for headers in common_headers_list:
            resolved_headers = resolve_variables(headers, {})
            global_headers.update(resolved_headers)
        
        # 初始化变量上下文
        variables_context = {}
        
        # 创建任务记录
        project_id = None
        if steps:
            # 从第一个步骤所属的测试用例获取项目 ID
            first_step = steps[0]
            test_case = TestCase.query.filter_by(id=first_step.case_id).first()
            if test_case:
                project_id = test_case.project_id
        
        task_name = "调试执行 - " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if case_id:
            test_case = TestCase.query.filter_by(id=case_id).first()
            if test_case:
                task_name = test_case.name + " - 执行"
        
        new_task = Task(
            project_id=project_id,
            case_id=case_id,
            env_id=env_id,
            name=task_name,
            creator_id=current_user.id,
            status='running',
            start_time=datetime.now(),
            log=json.dumps([]),
            total_steps=len(step_ids),
            pass_count=0,
            fail_count=0
        )
        db.session.add(new_task)
        db.session.flush()  # 获取 task_id
        
        # 执行步骤
        execution_log = []
        pass_count = 0
        fail_count = 0
        
        for step_id in step_ids:
            step = CaseStep.query.filter_by(id=step_id).first()
            if not step:
                continue
            
            # 执行单个步骤
            step_result = execute_single_step(step, env_base_url, variables_context, global_headers)
            execution_log.append(step_result)
            
            # 更新统计
            if step_result['passed']:
                pass_count += 1
            else:
                fail_count += 1
        
        # 完成任务
        end_time = datetime.now()
        duration = (end_time - new_task.start_time).total_seconds()
        status = 'success' if fail_count == 0 else 'failed'
        
        new_task.end_time = end_time
        new_task.duration = int(duration)
        new_task.status = status
        new_task.pass_count = pass_count
        new_task.fail_count = fail_count
        new_task.log = json.dumps(execution_log)
        
        db.session.commit()
        
        # 构建返回结果
        return {
            'code': 200,
            'msg': '执行完成',
            'data': {
                'task_id': new_task.id,
                'summary': {
                    'total_steps': len(step_ids),
                    'pass': pass_count,
                    'fail': fail_count,
                    'duration': duration
                },
                'log': execution_log
            }
        }
        
    except Exception as e:
        db.session.rollback()
        return {'code': 500, 'msg': f'执行失败: {str(e)}'}

@execution.route('/api/debug/run', methods=['POST'])
@login_required
def debug_run():
    """调试执行接口"""
    try:
        data = request.get_json()
        env_id = data.get('env_id')
        step_ids = data.get('step_ids')
        common_params_ids = data.get('common_params_ids', [])
        
        if not env_id:
            return jsonify({'code': 400, 'msg': 'env_id 不能为空'})
        
        if not step_ids or not isinstance(step_ids, list):
            return jsonify({'code': 400, 'msg': 'step_ids 不能为空且必须是数组'})
        
        # 调用公共执行函数
        result = run_steps(env_id, step_ids, common_params_ids)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'执行失败: {str(e)}'})

@execution.route('/api/cases/<int:case_id>/run', methods=['POST'])
@login_required
def run_case(case_id):
    """执行测试用例接口"""
    try:
        # 验证测试用例是否存在
        test_case = TestCase.query.filter_by(id=case_id).first()
        if not test_case:
            return jsonify({'code': 404, 'msg': '测试用例不存在'})
        
        data = request.get_json()
        env_id = data.get('env_id')
        common_params_ids = data.get('common_params_ids', [])
        
        if not env_id:
            return jsonify({'code': 400, 'msg': 'env_id 不能为空'})
        
        # 获取测试用例下所有启用的步骤，按排序升序
        steps = CaseStep.query.filter_by(case_id=case_id, enabled=True).order_by(CaseStep.sort).all()
        step_ids = [step.id for step in steps]
        
        if not step_ids:
            return jsonify({'code': 400, 'msg': '测试用例无启用的步骤'})
        
        # 调用公共执行函数
        result = run_steps(env_id, step_ids, common_params_ids, case_id)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'执行失败: {str(e)}'})

@execution.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task_detail(task_id):
    """查看单次执行报告详情"""
    try:
        # 查找任务
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'code': 404, 'msg': '任务不存在'})
        
        # 解析日志
        try:
            log = json.loads(task.log) if task.log else []
        except:
            log = []
        
        # 构建返回结果
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'task_id': task.id,
                'summary': {
                    'total_steps': task.total_steps,
                    'pass': task.pass_count,
                    'fail': task.fail_count,
                    'duration': task.duration
                },
                'log': log
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'获取任务详情失败: {str(e)}'})

@execution.route('/api/projects/<int:project_id>/reports', methods=['GET'])
@login_required
def get_project_reports(project_id):
    """获取项目下最近执行报告列表"""
    try:
        # 验证项目是否存在
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return jsonify({'code': 404, 'msg': '项目不存在'})
        
        # 查询项目下的任务，按创建时间倒序
        tasks = Task.query.filter_by(project_id=project_id).order_by(Task.created_at.desc()).limit(50).all()
        
        # 格式化报告数据
        reports = []
        for task in tasks:
            # 获取测试用例信息
            case_name = ''
            if task.case_id:
                test_case = TestCase.query.filter_by(id=task.case_id).first()
                if test_case:
                    case_name = test_case.name
            
            # 获取环境信息
            env_name = ''
            env = Env.query.filter_by(id=task.env_id).first()
            if env:
                env_name = env.name
            
            report = {
                'task_id': task.id,
                'case_id': task.case_id,
                'case_name': case_name,
                'env_id': task.env_id,
                'env_name': env_name,
                'status': task.status,
                'pass_count': task.pass_count,
                'fail_count': task.fail_count,
                'total_steps': task.total_steps,
                'duration': task.duration,
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            reports.append(report)
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'reports': reports
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'获取报告列表失败: {str(e)}'})