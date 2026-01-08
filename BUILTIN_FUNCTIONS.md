# 内置函数使用文档

## 概述

API 自动化测试平台提供了丰富的内置函数，用于生成测试数据、处理字符串、进行数学计算等操作。这些函数可以在测试用例的参数、头部、请求体等地方使用，通过 `${__函数名(参数1, 参数2)}` 的格式调用。

## 函数分类

### 1. 随机数据生成函数

| 函数名 | 描述 | 参数 | 示例 | 输出 |
|-------|------|------|------|------|
| `__random_plate` | 生成随机车牌 | 无 | `${__random_plate()}` | 京A12345 |
| `__random_phone` | 生成随机手机号 | 无 | `${__random_phone()}` | 13812345678 |
| `__random_string` | 生成随机字符串 | length: 字符串长度，默认8 | `${__random_string(10)}` | AbC123XyZ7 |
| `__random_string_with_prefix` | 生成带前缀的随机字符串 | prefix: 前缀，默认空<br>length: 总长度，默认8 | `${__random_string_with_prefix(ABC, 7)}` | ABC1234 |
| `__random_int` | 生成随机整数 | min_val: 最小值，默认1<br>max_val: 最大值，默认100 | `${__random_int(1, 1000)}` | 456 |
| `__random_float` | 生成随机浮点数 | min_val: 最小值，默认0<br>max_val: 最大值，默认100<br>decimal: 小数位数，默认2 | `${__random_float(0, 10, 3)}` | 3.141 |
| `__random_bool` | 生成随机布尔值 | 无 | `${__random_bool()}` | True |
| `__random_email` | 生成随机邮箱 | domain: 域名，默认example.com | `${__random_email(gmail.com)}` | abc123@gmail.com |
| `__random_ip` | 生成随机IP地址 | 无 | `${__random_ip()}` | 192.168.1.100 |
| `__random_mac` | 生成随机MAC地址 | 无 | `${__random_mac()}` | 00:11:22:33:44:55 |

### 2. 时间日期函数

| 函数名 | 描述 | 参数 | 示例 | 输出 |
|-------|------|------|------|------|
| `__timestamp` | 生成当前时间戳（秒） | 无 | `${__timestamp()}` | 1678901234 |
| `__timestamp_ms` | 生成当前时间戳（毫秒） | 无 | `${__timestamp_ms()}` | 1678901234567 |
| `__datetime` | 生成当前日期时间 | fmt: 时间格式，默认%Y-%m-%d %H:%M:%S | `${__datetime(%Y-%m-%d %H:%M:%S)}` | 2023-03-15 14:30:45 |
| `__date` | 生成当前日期 | fmt: 日期格式，默认%Y-%m-%d | `${__date(%Y/%m/%d)}` | 2023/03/15 |
| `__time` | 生成当前时间 | fmt: 时间格式，默认%H:%M:%S | `${__time(%H:%M:%S)}` | 14:30:45 |

### 3. UUID和唯一标识函数

| 函数名 | 描述 | 参数 | 示例 | 输出 |
|-------|------|------|------|------|
| `__uuid` | 生成UUID v4 | 无 | `${__uuid()}` | 123e4567-e89b-12d3-a456-426614174000 |
| `__uuid1` | 生成UUID v1 | 无 | `${__uuid1()}` | 123e4567-e89b-12d3-a456-426614174000 |
| `__uuid3` | 生成UUID v3（基于命名空间和名称） | namespace: 命名空间，默认ns:DNS<br>name: 名称，默认example.com | `${__uuid3(ns:DNS, test.com)}` | 123e4567-e89b-12d3-a456-426614174000 |
| `__uuid5` | 生成UUID v5（基于命名空间和名称） | namespace: 命名空间，默认ns:DNS<br>name: 名称，默认example.com | `${__uuid5(ns:DNS, test.com)}` | 123e4567-e89b-12d3-a456-426614174000 |

### 4. 字符串操作函数

| 函数名 | 描述 | 参数 | 示例 | 输出 |
|-------|------|------|------|------|
| `__lowercase` | 转换为小写 | text: 要转换的文本 | `${__lowercase(HELLO)}` | hello |
| `__uppercase` | 转换为大写 | text: 要转换的文本 | `${__uppercase(hello)}` | HELLO |
| `__capitalize` | 首字母大写 | text: 要转换的文本 | `${__capitalize(hello world)}` | Hello world |
| `__trim` | 去除首尾空格 | text: 要处理的文本 | `${__trim(  hello  )}` | hello |
| `__substring` | 截取子字符串 | text: 原始文本<br>start: 开始位置，默认0<br>end: 结束位置，默认全部 | `${__substring(hello world, 0, 5)}` | hello |

### 5. 数学计算函数

| 函数名 | 描述 | 参数 | 示例 | 输出 |
|-------|------|------|------|------|
| `__add` | 加法运算 | a: 第一个数<br>b: 第二个数 | `${__add(1, 2)}` | 3 |
| `__subtract` | 减法运算 | a: 被减数<br>b: 减数 | `${__subtract(5, 2)}` | 3 |
| `__multiply` | 乘法运算 | a: 第一个数<br>b: 第二个数 | `${__multiply(2, 3)}` | 6 |
| `__divide` | 除法运算 | a: 被除数<br>b: 除数 | `${__divide(10, 2)}` | 5 |
| `__modulus` | 取模运算 | a: 被除数<br>b: 除数 | `${__modulus(10, 3)}` | 1 |

### 6. 其他工具函数

| 函数名 | 描述 | 参数 | 示例 | 输出 |
|-------|------|------|------|------|
| `__url_encode` | URL编码 | text: 要编码的文本 | `${__url_encode(hello world)}` | hello%20world |
| `__url_decode` | URL解码 | text: 要解码的文本 | `${__url_decode(hello%20world)}` | hello world |
| `__json_encode` | JSON编码 | obj: 要编码的对象 | `${__json_encode({"name": "test"})}` | {"name": "test"} |
| `__json_decode` | JSON解码 | text: 要解码的JSON字符串 | `${__json_decode({"name": "test"})}` | {"name": "test"} |

## 使用示例

### 1. 在请求参数中使用

```json
{
  "user_id": "${__random_int(1000, 9999)}",
  "user_name": "${__random_string(8)}",
  "email": "${__random_email()}",
  "register_time": "${__datetime()}"
}
```

### 2. 在请求头部中使用

```json
{
  "X-Request-ID": "${__uuid()}",
  "X-Timestamp": "${__timestamp()}",
  "User-Agent": "Test-Agent-${__random_string(6)}"
}
```

### 3. 在请求体中使用

```json
{
  "order": {
    "id": "${__uuid()}",
    "amount": "${__random_float(10, 1000, 2)}",
    "currency": "CNY",
    "created_at": "${__datetime()}",
    "items": [
      {
        "id": "${__random_int(1, 100)}",
        "name": "Product ${__random_string(5)}",
        "price": "${__random_float(1, 100, 2)}",
        "quantity": "${__random_int(1, 10)}"
      }
    ]
  }
}
```

### 4. 在变量提取表达式中使用

```json
{
  "var_name": "order_id",
  "expression": "$.order.id",
  "var_type": "string"
}
```

### 5. 嵌套使用函数

```json
{
  "user_id": "${__add(${__random_int(1000, 9999)}, 10000)}",
  "timestamp": "${__subtract(${__timestamp()}, 3600)}",
  "unique_id": "${__uppercase(${__uuid()})}"
}
```

## 注意事项

1. 所有函数的参数都可以使用变量替换，例如：`${__random_int(${min_val}, ${max_val})}`
2. 函数调用的格式必须是 `${__函数名(参数1, 参数2)}`，其中参数之间用逗号分隔
3. 对于需要引号的参数值，应使用单引号或双引号包围，例如：`${__random_email('gmail.com')}`
4. 如果函数执行失败，将返回原始的函数调用字符串，例如：`${__nonexistent_function()}`
5. 函数返回值的类型都是字符串，在使用时需要根据实际情况进行类型转换