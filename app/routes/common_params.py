from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.common_params import CommonParams
from app import db
from datetime import datetime
import json

def get_builtin_functions_info():
    return {
        "categories": [
            {
                "name": "随机数据生成",
                "functions": [
                    {
                        "name": "__random_plate",
                        "description": "生成随机车牌",
                        "params": [],
                        "example": "${__random_plate()}",
                        "output": "京A12345"
                    },
                    {
                        "name": "__random_phone",
                        "description": "生成随机手机号",
                        "params": [],
                        "example": "${__random_phone()}",
                        "output": "13812345678"
                    },
                    {
                        "name": "__random_string",
                        "description": "生成随机字符串",
                        "params": [
                            {"name": "length", "default": "8", "description": "字符串长度"}
                        ],
                        "example": "${__random_string(10)}",
                        "output": "AbC123XyZ7"
                    },
                    {
                        "name": "__random_string_with_prefix",
                        "description": "生成带前缀的随机字符串",
                        "params": [
                            {"name": "prefix", "default": "", "description": "前缀字符串"},
                            {"name": "length", "default": "8", "description": "总长度"}
                        ],
                        "example": "${__random_string_with_prefix(ABC, 7)}",
                        "output": "ABC1234"
                    },
                    {
                        "name": "__random_int",
                        "description": "生成随机整数",
                        "params": [
                            {"name": "min_val", "default": "1", "description": "最小值"},
                            {"name": "max_val", "default": "100", "description": "最大值"}
                        ],
                        "example": "${__random_int(1, 1000)}",
                        "output": "456"
                    },
                    {
                        "name": "__random_float",
                        "description": "生成随机浮点数",
                        "params": [
                            {"name": "min_val", "default": "0", "description": "最小值"},
                            {"name": "max_val", "default": "100", "description": "最大值"},
                            {"name": "decimal", "default": "2", "description": "小数位数"}
                        ],
                        "example": "${__random_float(0, 10, 3)}",
                        "output": "3.141"
                    },
                    {
                        "name": "__random_bool",
                        "description": "生成随机布尔值",
                        "params": [],
                        "example": "${__random_bool()}",
                        "output": "True"
                    },
                    {
                        "name": "__random_email",
                        "description": "生成随机邮箱",
                        "params": [
                            {"name": "domain", "default": "example.com", "description": "域名"}
                        ],
                        "example": "${__random_email(gmail.com)}",
                        "output": "abc123@gmail.com"
                    },
                    {
                        "name": "__random_ip",
                        "description": "生成随机IP地址",
                        "params": [],
                        "example": "${__random_ip()}",
                        "output": "192.168.1.100"
                    },
                    {
                        "name": "__random_mac",
                        "description": "生成随机MAC地址",
                        "params": [],
                        "example": "${__random_mac()}",
                        "output": "00:11:22:33:44:55"
                    }
                ]
            },
            {
                "name": "时间日期",
                "functions": [
                    {
                        "name": "__timestamp",
                        "description": "生成当前时间戳（秒）",
                        "params": [],
                        "example": "${__timestamp()}",
                        "output": "1678901234"
                    },
                    {
                        "name": "__timestamp_ms",
                        "description": "生成当前时间戳（毫秒）",
                        "params": [],
                        "example": "${__timestamp_ms()}",
                        "output": "1678901234567"
                    },
                    {
                        "name": "__datetime",
                        "description": "生成当前日期时间",
                        "params": [
                            {"name": "fmt", "default": "%Y-%m-%d %H:%M:%S", "description": "时间格式"}
                        ],
                        "example": "${__datetime(%Y-%m-%d %H:%M:%S)}",
                        "output": "2023-03-15 14:30:45"
                    },
                    {
                        "name": "__date",
                        "description": "生成当前日期",
                        "params": [
                            {"name": "fmt", "default": "%Y-%m-%d", "description": "日期格式"}
                        ],
                        "example": "${__date(%Y/%m/%d)}",
                        "output": "2023/03/15"
                    },
                    {
                        "name": "__time",
                        "description": "生成当前时间",
                        "params": [
                            {"name": "fmt", "default": "%H:%M:%S", "description": "时间格式"}
                        ],
                        "example": "${__time(%H:%M:%S)}",
                        "output": "14:30:45"
                    }
                ]
            },
            {
                "name": "UUID和唯一标识",
                "functions": [
                    {
                        "name": "__uuid",
                        "description": "生成UUID v4",
                        "params": [],
                        "example": "${__uuid()}",
                        "output": "123e4567-e89b-12d3-a456-426614174000"
                    },
                    {
                        "name": "__uuid1",
                        "description": "生成UUID v1",
                        "params": [],
                        "example": "${__uuid1()}",
                        "output": "123e4567-e89b-12d3-a456-426614174000"
                    },
                    {
                        "name": "__uuid3",
                        "description": "生成UUID v3（基于命名空间和名称）",
                        "params": [
                            {"name": "namespace", "default": "ns:DNS", "description": "命名空间"},
                            {"name": "name", "default": "example.com", "description": "名称"}
                        ],
                        "example": "${__uuid3(ns:DNS, test.com)}",
                        "output": "123e4567-e89b-12d3-a456-426614174000"
                    },
                    {
                        "name": "__uuid5",
                        "description": "生成UUID v5（基于命名空间和名称）",
                        "params": [
                            {"name": "namespace", "default": "ns:DNS", "description": "命名空间"},
                            {"name": "name", "default": "example.com", "description": "名称"}
                        ],
                        "example": "${__uuid5(ns:DNS, test.com)}",
                        "output": "123e4567-e89b-12d3-a456-426614174000"
                    }
                ]
            },
            {
                "name": "字符串操作",
                "functions": [
                    {
                        "name": "__lowercase",
                        "description": "转换为小写",
                        "params": [
                            {"name": "text", "description": "要转换的文本"}
                        ],
                        "example": "${__lowercase(HELLO)}",
                        "output": "hello"
                    },
                    {
                        "name": "__uppercase",
                        "description": "转换为大写",
                        "params": [
                            {"name": "text", "description": "要转换的文本"}
                        ],
                        "example": "${__uppercase(hello)}",
                        "output": "HELLO"
                    },
                    {
                        "name": "__capitalize",
                        "description": "首字母大写",
                        "params": [
                            {"name": "text", "description": "要转换的文本"}
                        ],
                        "example": "${__capitalize(hello world)}",
                        "output": "Hello world"
                    },
                    {
                        "name": "__trim",
                        "description": "去除首尾空格",
                        "params": [
                            {"name": "text", "description": "要处理的文本"}
                        ],
                        "example": "${__trim(  hello  )}",
                        "output": "hello"
                    },
                    {
                        "name": "__substring",
                        "description": "截取子字符串",
                        "params": [
                            {"name": "text", "description": "原始文本"},
                            {"name": "start", "default": "0", "description": "开始位置"},
                            {"name": "end", "description": "结束位置，默认全部"}
                        ],
                        "example": "${__substring(hello world, 0, 5)}",
                        "output": "hello"
                    }
                ]
            },
            {
                "name": "数学计算",
                "functions": [
                    {
                        "name": "__add",
                        "description": "加法运算",
                        "params": [
                            {"name": "a", "description": "第一个数"},
                            {"name": "b", "description": "第二个数"}
                        ],
                        "example": "${__add(1, 2)}",
                        "output": "3"
                    },
                    {
                        "name": "__subtract",
                        "description": "减法运算",
                        "params": [
                            {"name": "a", "description": "被减数"},
                            {"name": "b", "description": "减数"}
                        ],
                        "example": "${__subtract(5, 2)}",
                        "output": "3"
                    },
                    {
                        "name": "__multiply",
                        "description": "乘法运算",
                        "params": [
                            {"name": "a", "description": "第一个数"},
                            {"name": "b", "description": "第二个数"}
                        ],
                        "example": "${__multiply(2, 3)}",
                        "output": "6"
                    },
                    {
                        "name": "__divide",
                        "description": "除法运算",
                        "params": [
                            {"name": "a", "description": "被除数"},
                            {"name": "b", "description": "除数"}
                        ],
                        "example": "${__divide(10, 2)}",
                        "output": "5"
                    },
                    {
                        "name": "__modulus",
                        "description": "取模运算",
                        "params": [
                            {"name": "a", "description": "被除数"},
                            {"name": "b", "description": "除数"}
                        ],
                        "example": "${__modulus(10, 3)}",
                        "output": "1"
                    }
                ]
            },
            {
                "name": "其他工具函数",
                "functions": [
                    {
                        "name": "__url_encode",
                        "description": "URL编码",
                        "params": [
                            {"name": "text", "description": "要编码的文本"}
                        ],
                        "example": "${__url_encode(hello world)}",
                        "output": "hello%20world"
                    },
                    {
                        "name": "__url_decode",
                        "description": "URL解码",
                        "params": [
                            {"name": "text", "description": "要解码的文本"}
                        ],
                        "example": "${__url_decode(hello%20world)}",
                        "output": "hello world"
                    },
                    {
                        "name": "__json_encode",
                        "description": "JSON编码",
                        "params": [
                            {"name": "obj", "description": "要编码的对象"}
                        ],
                        "example": "${__json_encode({\"name\": \"test\"})}",
                        "output": "{\"name\": \"test\"}"
                    },
                    {
                        "name": "__json_decode",
                        "description": "JSON解码",
                        "params": [
                            {"name": "text", "description": "要解码的JSON字符串"}
                        ],
                        "example": "${__json_decode({\"name\": \"test\"})}",
                        "output": "{\"name\": \"test\"}"
                    }
                ]
            }
        ]
    }

common_params = Blueprint('common_params', __name__)

@common_params.route('/api/common-params', methods=['GET'])
@login_required
def get_common_params():
    try:
        # 获取查询参数
        project_id = request.args.get('project_id', type=int)
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        # 构建查询
        query = CommonParams.query
        
        # 只获取当前用户创建的参数
        query = query.filter_by(creator_id=current_user.id)
        
        # 如果指定了项目ID，则过滤
        if project_id is not None:
            query = query.filter_by(project_id=project_id)
        else:
            # 否则获取全局参数（project_id为null）和所有项目级参数
            query = query
        
        # 执行查询
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        
        # 格式化数据
        params_data = []
        from app.models.user import User
        for params in pagination.items:
            # 获取创建人昵称
            creator_nickname = ''
            creator = User.query.filter_by(id=params.creator_id).first()
            if creator:
                creator_nickname = creator.nickname or creator.username
            
            params_data.append({
                'id': params.id,
                'project_id': params.project_id,
                'name': params.name,
                'headers': json.loads(params.headers),
                'description': params.description,
                'creator_id': params.creator_id,
                'creator_name': creator_nickname,
                'created_at': params.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'common_params': params_data,
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

@common_params.route('/api/builtin-functions', methods=['GET'])
@login_required
def get_builtin_functions():
    try:
        functions_info = get_builtin_functions_info()
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': functions_info
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取内置函数失败: {str(e)}'
        })