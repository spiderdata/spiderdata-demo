import uuid
from flask import g, Flask, jsonify, make_response, request
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

token_auth = HTTPTokenAuth('Token')

# TODO: 需要使用数据库存储用户信息
# users = [{'username': 'Tom', 'password': '123456'}]
users = []

# TODO: 需要用数据库存储用户Token
# tokens: {'xxxxxxx': 'username'}
tokens = {}

jobs = {
    'python': 30,
    'java': 35,
    'c++': 25
}


@app.route('/api/user/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # 确认用户名和密码是否存在
    if username is None or password is None:
        resp = {'msg': 'username or password is null',
                'status': 10003,
                'body': {}}
        return make_response(jsonify(resp), 400)

    # TODO: 用户名、密码合法性检查

    # 判断用户是否存在
    if user_exist(username):
        resp = {'msg': 'User exists',
                'status': 10002,
                'body': {}}
        return make_response(jsonify(resp), 400)

    user = add_user(username, password)
    resp = {'msg': 'OK',
            'status': 10001,
            'body': {'username': user['username']}}
    return make_response(jsonify(resp), 201)


@app.route('/api/user/login', methods=['POST'])
def login():
    # 从请求中获取用户名和密码
    username = request.json.get('username')
    password = request.json.get('password')

    # 确认用户名和密码是否存在
    if username is None or password is None:
        resp = {'msg': 'username or password is null',
                'status': 10003,
                'body': {}}
        return make_response(jsonify(resp), 400)

    # 判断用户是否存在
    if not user_exist(username):
        resp = {'msg': 'User not exists',
                'status': 10004,
                'body': {}}
        return make_response(jsonify(resp), 404)

    # 验证密码是否正确
    if not verify_password(username, password):
        resp = {'msg': 'Password not correct',
                'status': 10005,
                'body': {}}
        return make_response(jsonify(resp), 400)

    token = generate_auth_token()
    tokens[token] = username
    resp = {'msg': 'Login successfully',
            'status': 10001,
            'body': {'token': token}}
    return jsonify(resp), 201


@app.route('/api/user/change_password', methods=['PUT'])
@token_auth.login_required
def change_password():
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    # TODO: 调用 User 对象的修改密码的方法
    if not check_password(g.user, old_password):
        resp = {'msg': 'Old password not correct',
                'status': 10005,
                'body': {}}
        return make_response(jsonify(resp), 400)
    update_password(g.user, new_password)
    resp = {'msg': 'Change password successfully',
            'status': 10001,
            'body': {'username': g.user}}
    return make_response(jsonify(resp), 201)


@app.route('/api/data/jobs', methods=['GET'])
@token_auth.login_required
def get_jobs_data():
    # TODO: 该接口应该放在 spiderdata_demon/data/api.py 中
    # TODO: 数据需要从数据库获取
    language = request.json.get('language')
    # TODO: 处理 language 为空的问题
    resp = {'msg': 'OK',
            'status': 20001,
            'body': {'jobs': {language: jobs[language]}}}
    return make_response(jsonify(resp), 201)


@token_auth.verify_token
def verify_token(token):
    g.user = None
    if token in tokens:
        g.user = tokens[token]
        return True
    return False


# TODO: 下面这些方法需要写到 User 类里
def user_exist(username):
    for u in users:
        if username == u['username']:
            return True
    return False


def add_user(username, password):
    user = {'username': username, 'password': password}
    users.append(user)
    return user


def check_password(username, password):
    passwd = None
    for u in users:
        if u['username'] == username:
            passwd = u['password']
    if password == passwd:
        return True
    return False


def update_password(username, password):
    for u in users:
        if u['username'] == username:
            u['password'] = password


def generate_auth_token(expiration = 600):
    token = str(uuid.uuid4())
    return token


def verify_password(username, password):
    # TODO: g.user 中存放 User 类实例化的 user 对象
    g.user = username
    if not user_exist(username) or not check_password(username, password):
        return False
    return True
