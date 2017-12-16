#coding=utf-8
# 作用：接收微信服务器的信息
from flask import Flask

app = Flask(__name__)

from flask import request, jsonify
from hashlib import sha1
# import xmltodict
from time import time
#如果当前账户为s8014，则路由为/wechat8014，启动端口为port=8014
#?signature=2023d54455f0871a3fb05fa9beb3465986b26ef4
# &echostr=2071637787555134447
# &timestamp=1513150604
# &nonce=3197783795
#身份验证
def auth():
    # 1.接收微信服务器发送过开的数据
    dict = request.args
    signature = dict.get('signature')
    timestamp = dict.get('timestamp')
    nonce = dict.get('nonce')
    # 如果数据不完整，不是微信的请求，直接返回
    if not all([signature, timestamp, nonce]):
        return jsonify(msg='参数不完整'), 404
    # 2.排序
    token = 'lunzipo'
    list1 = [token, timestamp, nonce]
    list1.sort()
    # 3.加密
    str1 = ''.join(list1)
    s1 = sha1()
    s1.update(str1)
    str2 = s1.hexdigest()
    # 4、验证
    if str2 == signature:
        return True
    else:
        return jsonify(msg='服务器错误'), 404


# get请求方式：服务器认证
@app.route('/weixin', methods=['GET'])
def wechat():
    auth_ret = auth()
    if auth_ret==True:
        return request.args.get('echostr')
    else:
        return auth_ret


if __name__ == '__main__':
    app.run()
