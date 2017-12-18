#coding=utf-8
# 作用：接收微信服务器的信息
from flask import Flask

app = Flask(__name__)

from flask import request, jsonify
from hashlib import sha1
import xmltodict
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


'''
request接收数据：
request.args:用于接收get方式的请求，格式为键值对
request.form:用于接收post方式的请求，格式为键值对
request.data:用于接收请求，格式为非键值对
request.files:用于接收文件
'''

#POST请求方式：接收微信的请求
@app.route('/weixin',methods=['POST'])
def msg_handle():
    auth_ret=auth()
    if auth_ret==True:
        #接收xml数据
        xml_data=request.data
        #转成dict数据
        dict_data=xmltodict.parse(xml_data)
        #获取根数据xml
        xml=dict_data.get('xml')
        #数据类型判断
        if xml.get('MsgType')=='text':#文本
            #当前消息是文本类型
            # print xml.get('Content')
            #<xml> <ToUserName><![CDATA[toUser]]></ToUserName> <FromUserName><![CDATA[fromUser]]></FromUserName> <CreateTime>12345678</CreateTime> <MsgType><![CDATA[text]]></MsgType> <Content><![CDATA[你好]]></Content> </xml>
            #根据文档格式构造数据dict
            dict_ret={'ToUserName':xml.get('FromUserName'),
                      'FromUserName':xml.get('ToUserName'),
                      'CreateTime':int(time()),
                      'MsgType':'text',
                      'Content':xml.get('Content')+u'，你美你说的都对'}
            #将dict转换成xml
            xml_ret=xmltodict.unparse({'xml':dict_ret})
            #返回
            return xml_ret
        elif xml.get('MsgType')=='event':
            dict_ret={'ToUserName':xml.get('FromUserName'),
                      'FromUserName':xml.get('ToUserName'),
                      'CreateTime':int(time()),
                      'MsgType':'text',
                      'Content':xml.get('EventKey')
                  }
            #将dict转换成xml
            xml_ret=xmltodict.unparse({'xml':dict_ret})
            #返回
            return xml_ret
        else:
            pass
    else:
        return auth_ret


if __name__ == '__main__':
    app.run()
