from flask import Flask,render_template,request
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json

app = Flask(__name__)

USERS = {
    '1':{'name':'钢弹','count':0},
    '2':{'name':'铁锤','count':0},
    '3':{'name':'贝贝','count':100},
}


WEBSOCKET_LIST = {}


@app.route('/message/<src_user>/<dest_user>')
# @token_auth.login_required
def message(src_user, dest_user):
    ws = request.environ.get('wsgi.websocket')
    # print(ws)
    if not ws:
        print('http')
        return '您使用的是Http协议'
    WEBSOCKET_LIST[src_user] = ws
    print(WEBSOCKET_LIST)
    print('---------------------1-------------')
    while True:
        cid = ws.receive()  # 接收信息
        if not cid:
            del WEBSOCKET_LIST[src_user]
            ws.close()
            break
        print(cid)
        for user_name, user_socket in WEBSOCKET_LIST.items():
            if user_name == dest_user:
                user_socket.send(cid)

            # msg_from={
            #     "send_user":username,
            #     "send_msg":user_msg
            # }
            # if user_socket == user_socket:
            #     continue
            # user_socket.send(json.dumps(msg_from))

            # WEBSOCKET_LIST.pop(user_name)


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()