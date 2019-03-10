# spiderdata 项目 demo

通过 Flask 实现 RESTful API 示例


## 安装方法

* 下载代码到本地

```
$ git clone https://github.com/spiderdata/spiderdata-demo.git
```

* 切换工作目录

```
$ cd spiderdata-demo
```

* 将 spiderdata-demo 安装到系统中

```
$ sudo python3 setup.py install
```

## 使用方法

* 启动服务器

```
$ python3 spiderdata_demo/cmd/user_api.py
 * Serving Flask app "spiderdata_demo.server.user.api" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## API 调用示例

#### 用户注册

* API

```
/v1/users
```

* Http Method

```
POST
```

* 请求头

```
Content-Type: application/json
```

* 请求参数

|键|数据类型|功能|
|----|----|----|
|username|str|用户名|
|password|str|密码|

* 返回数据

|键|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|


|键|数据类型|功能|
|----|----|----|
|username|str|用户名|

* 请求示例

```
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"Jerry","password":"happy123"}' http://127.0.0.1:5000/v1/users | python3 -m json.tool

{
    "body": {
        "username": "Jerry"
    },
    "msg": "OK",
    "status": 10001
}
```

#### 获取用户token(登陆)

* API

```
/v1/auth/tokens
```

* Http Method

```
POST
```

* 请求头

```
Content-Type: application/json
```

* 请求参数

|键|数据类型|功能|
|----|----|----|
|username|str|用户名|
|password|str|密码|

* 返回数据

|键|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|


|键|数据类型|功能|
|----|----|----|
|token|str|用户token，用于后续其它请求时的用户认证|

* 请求示例

```
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"Jerry","password":"happy123"}' http://127.0.0.1:5000/v1/auth/tokens | python3 -m json.tool

{
    "body": {
        "token": "3dac945a-5151-431f-845d-c1bf57a8038e"
    },
    "msg": "Login successfully",
    "status": 10001
}

```

#### 获取数据

* API

```
/v1/data/jobs
```

* Http Method

```
GET
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|键|数据类型|功能|
|----|----|----|
|language|str|语言名(e.g. python)|

* 返回数据

|键|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|


|键|数据类型|功能|
|----|----|----|
|jobs|dict|查询到的指定语言的工作数|

* 请求示例

> 注意：需要通过请求头传递登陆时获取到的 token，例如：
>
> -H "Authorization: Token 3dac945a-5151-431f-845d-c1bf57a8038e"

```
$ curl -X GET -H "Content-Type: application/json" -H "Authorization: Token 3dac945a-5151-431f-845d-c1bf57a8038e" -d '{"language":"python"}' http://127.0.0.1:5000/v1/data/jobs | python3 -m json.tool

{
    "body": {
        "jobs": {
            "python": 30
        }
    },
    "msg": "OK",
    "status": 20001
}
```

#### 用户修改密码

* API

```
/v1/users/password
```

* Http Method

```
PUT
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|键|数据类型|功能|
|----|----|----|
|old_password|str|旧密码|
|new_password|str|新密码|

* 返回数据

|键|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|


|键|数据类型|功能|
|----|----|----|
|username|str|修改密码用户的用户名|

* 请求示例

```
$ curl -X PUT -H "Content-Type: application/json" -H "Authorization: Token 3dac945a-5151-431f-845d-c1bf57a8038e" -d '{"old_password":"happy123","new_password":"tarena123"}' http://127.0.0.1:5000/v1/users/password | python3 -m json.tool

{
    "body": {
        "username": "Jerry"
    },
    "msg": "Change password successfully",
    "status": 10001
}
```
