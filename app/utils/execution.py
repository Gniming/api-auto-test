import random
import string
import re
import json
import requests
import uuid
from datetime import datetime

# 内置函数映射字典
BUILTIN_FUNCTIONS = {
    '__random_plate': lambda: generate_random_plate(),
    '__random_phone': lambda: generate_random_phone(),
    '__random_string': lambda length=8: ''.join(random.choices(string.ascii_letters + string.digits, k=int(length or 8))),
    '__random_int': lambda min_val=1, max_val=100: str(random.randint(int(min_val), int(max_val))),
    '__timestamp': lambda: str(int(datetime.now().timestamp())),
    '__date': lambda fmt='%Y-%m-%d': datetime.now().strftime(fmt or '%Y-%m-%d'),
    '__uuid': lambda: str(uuid.uuid4()),
}

def generate_random_plate():
    """生成随机车牌"""
    provinces = ['京', '沪', '粤', '苏', '浙', '鲁', '豫', '川', '冀', '晋', '辽', '吉', '黑', '皖', '闽', '赣', '湘', '鄂', '贵', '云', '陕', '甘', '青', '琼', '渝', '津', '蒙', '宁', '新', '藏']
    province = random.choice(provinces)
    letters = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.digits, k=5))
    return f"{province}{letters}{numbers}"

def generate_random_phone():
    """生成随机手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152', '153', '155', '156', '157', '158', '159', '170', '171', '172', '173', '175', '176', '177', '178', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}{suffix}"

def resolve_variables(text, variables_context=None):
    """
    变量替换函数
    参数：text (str or dict or list) - 要替换的字符串、JSON 对象或数组
    功能：支持嵌套替换，先替换内置函数，再替换变量
    """
    if variables_context is None:
        variables_context = {}
    
    def replace_var(match):
        content = match.group(1).strip()
        # 检查是否是内置函数调用
        if content.startswith('__'):
            # 解析函数名和参数
            func_match = re.match(r'(\w+)(?:\((.*)\))?', content)
            if func_match:
                func_name = func_match.group(1)
                args_str = func_match.group(2) or ''
                
                if func_name in BUILTIN_FUNCTIONS:
                    # 解析参数
                    args = []
                    kwargs = {}
                    if args_str:
                        # 简单的参数解析，不支持嵌套
                        param_tokens = [p.strip() for p in args_str.split(',') if p.strip()]
                        for param in param_tokens:
                            if '=' in param:
                                key, val = param.split('=', 1)
                                kwargs[key.strip()] = val.strip()
                            else:
                                args.append(param.strip())
                    
                    # 执行函数
                    try:
                        if args:
                            return BUILTIN_FUNCTIONS[func_name](*args)
                        elif kwargs:
                            return BUILTIN_FUNCTIONS[func_name](**kwargs)
                        else:
                            return BUILTIN_FUNCTIONS[func_name]()
                    except Exception:
                        return match.group(0)
        # 普通变量
        elif content in variables_context:
            return str(variables_context[content])
        return match.group(0)
    
    if isinstance(text, str):
        # 先替换内置函数
        result = re.sub(r'\$\{([^}]+)\}', replace_var, text)
        # 再替换变量（以防内置函数返回的内容中包含变量）
        result = re.sub(r'\$\{([^}]+)\}', replace_var, result)
        return result
    elif isinstance(text, dict):
        return {key: resolve_variables(value, variables_context) for key, value in text.items()}
    elif isinstance(text, list):
        return [resolve_variables(item, variables_context) for item in text]
    else:
        return text

def merge_headers(common_headers_list, step_headers, variables_context=None):
    """
    headers 合并函数
    common_headers_list：从 common_params_ids 加载的多个 headers dict 列表
    step_headers：步骤的 headers dict
    返回最终合并后的 headers dict
    """
    if variables_context is None:
        variables_context = {}
    
    merged_headers = {}
    
    # 按顺序合并公共 headers
    for headers in common_headers_list:
        # 先进行变量替换
        resolved_headers = resolve_variables(headers, variables_context)
        # 合并到结果中
        merged_headers.update(resolved_headers)
    
    # 最后合并步骤 headers（优先级最高）
    if step_headers:
        resolved_step_headers = resolve_variables(step_headers, variables_context)
        merged_headers.update(resolved_step_headers)
    
    return merged_headers

def execute_single_step(step, env_base_url, variables_context=None, global_headers=None):
    """
    执行单个步骤函数
    step：步骤对象
    env_base_url：环境基础 URL
    variables_context：变量上下文
    global_headers：全局 headers
    返回步骤执行结果 dict
    """
    if variables_context is None:
        variables_context = {}
    if global_headers is None:
        global_headers = {}
    
    # 构建完整 URL
    full_url = env_base_url.rstrip('/') + '/' + step.path.lstrip('/')
    
    # 加载请求数据
    from app.models.request_data import RequestData
    request_data = RequestData.query.filter_by(step_id=step.id).first()
    
    # 初始化请求参数
    headers = {}
    params = {}
    data = {}
    timeout = 30
    files = None
    
    if request_data:
        # 解析并替换变量
        if request_data.headers:
            try:
                headers = json.loads(request_data.headers)
            except:
                headers = {}
        if request_data.params:
            try:
                params = json.loads(request_data.params)
            except:
                params = {}
        if request_data.data:
            try:
                data = json.loads(request_data.data)
            except:
                data = {}
        if request_data.files:
            try:
                files = json.loads(request_data.files)
            except:
                files = None
        timeout = request_data.timeout or 30
    
    # 变量替换
    headers = resolve_variables(headers, variables_context)
    params = resolve_variables(params, variables_context)
    data = resolve_variables(data, variables_context)
    
    # 合并 headers
    merged_headers = merge_headers([global_headers], headers, variables_context)
    
    # 准备请求
    request_kwargs = {
        'method': step.method or 'GET',
        'url': full_url,
        'headers': merged_headers,
        'params': params,
        'timeout': timeout,
        'allow_redirects': True
    }
    
    # 根据 content-type 自动判断请求体格式
    content_type = merged_headers.get('Content-Type', '')
    if 'application/json' in content_type:
        request_kwargs['json'] = data
    else:
        request_kwargs['data'] = data
    
    if files:
        request_kwargs['files'] = files
    
    # 发送请求
    request_info = {
        'url': full_url,
        'method': step.method or 'GET',
        'headers': merged_headers,
        'params': params,
        'data': data
    }
    
    response_info = {
        'status_code': None,
        'headers': {},
        'text': '',
        'elapsed': 0
    }
    
    extract_results = {}
    assert_results = []
    passed = True
    
    try:
        start_time = datetime.now()
        response = requests.request(**request_kwargs)
        end_time = datetime.now()
        
        # 记录响应信息
        response_info['status_code'] = response.status_code
        response_info['headers'] = dict(response.headers)
        response_info['text'] = response.text
        response_info['elapsed'] = (end_time - start_time).total_seconds()
        
        # 执行变量提取
        from app.models.extract import Extract
        extracts = Extract.query.filter_by(step_id=step.id).all()
        for extract in extracts:
            var_name = extract.var_name
            expression = extract.expression
            try:
                # 简单的 JSONPath 实现，这里使用正则匹配
                if expression.startswith('$.'):
                    # 尝试解析 JSON
                    try:
                        json_data = response.json()
                        # 简单的 JSONPath 解析
                        keys = expression[2:].split('.')
                        value = json_data
                        for key in keys:
                            if isinstance(value, dict) and key in value:
                                value = value[key]
                            else:
                                value = None
                                break
                        if value is not None:
                            extract_results[var_name] = value
                            variables_context[var_name] = value
                    except:
                        pass
                else:
                    # 正则提取
                    match = re.search(expression, response.text)
                    if match:
                        extract_results[var_name] = match.group(0)
                        variables_context[var_name] = match.group(0)
            except Exception:
                pass
        
        # 执行断言
        from app.models.assert_rule import AssertRule
        asserts = AssertRule.query.filter_by(step_id=step.id).all()
        for assert_rule in asserts:
            assert_type = assert_rule.assert_type
            expect_value = assert_rule.expect_value
            actual_source = assert_rule.actual_source or 'response_body'
            
            actual_value = ''
            if actual_source == 'response_status':
                actual_value = str(response.status_code)
            elif actual_source == 'response_headers':
                actual_value = str(dict(response.headers))
            elif actual_source == 'response_body':
                actual_value = response.text
            elif actual_source.startswith('$'):
                # JSONPath 表达式，从响应中提取值
                try:
                    json_data = response.json()
                    # 简单的 JSONPath 解析
                    keys = actual_source[2:].split('.') if actual_source.startswith('$.') else actual_source[1:].split('.')
                    value = json_data
                    for key in keys:
                        if isinstance(value, dict) and key in value:
                            value = value[key]
                        else:
                            value = None
                            break
                    actual_value = str(value) if value is not None else ''
                except:
                    actual_value = ''
            
            assert_passed = False
            try:
                if assert_type == 'status_code':
                    assert_passed = str(response.status_code) == expect_value
                elif assert_type == 'contain':
                    assert_passed = expect_value in actual_value
                elif assert_type == 'not_contain':
                    assert_passed = expect_value not in actual_value
                elif assert_type == 'json_equal':
                    try:
                        expect_json = json.loads(expect_value)
                        actual_json = response.json()
                        assert_passed = expect_json == actual_json
                    except:
                        assert_passed = False
                elif assert_type == 'regex':
                    assert_passed = bool(re.search(expect_value, actual_value))
                elif assert_type == 'length':
                    assert_passed = str(len(actual_value)) == expect_value
                else:
                    assert_passed = False
            except Exception:
                assert_passed = False
            
            assert_results.append({
                'type': assert_type,
                'expect': expect_value,
                'actual': actual_value,
                'passed': assert_passed
            })
            
            if not assert_passed:
                passed = False
                
    except Exception as e:
        response_info['text'] = str(e)
        passed = False
    
    # 构建执行结果
    result = {
        'step_id': step.id,
        'step_name': step.name,
        'request': request_info,
        'response': response_info,
        'extract_results': extract_results,
        'assert_results': assert_results,
        'passed': passed
    }
    
    return result