# -*- coding: utf-8 -*-

import web
import hashlib
import reply
import receive

class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return 'Hello this is not hot-plug handle view'
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = 'wechatwebapp20191215'

            compose_list = [token, timestamp, nonce]
            compose_list.sort()
            sha1 = hashlib.sha1()

            # should comment map function as it only works in py2
            # map(sha1.update, compose_list)

            # should use below for py3 refer to below url
            # https://www.cnblogs.com/roadwide/p/10566946.html

            sha1.update(compose_list[0].encode('utf-8'))
            sha1.update(compose_list[1].encode('utf-8'))
            sha1.update(compose_list[2].encode('utf-8'))
            hashcode = sha1.hexdigest()

            print("handle/GET func: hashcode, signature: ", hashcode, signature)
        except Exception as e:
            print('error type:', type(e))
            print('error value:', e)
            return e
        else:
            if hashcode == signature:
                return echostr
            else:
                return ''

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is:", webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "post test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print("Non text data.")
                return "success"
        except Exception as e:
            print("error type:", type(e))
            print("error value:", e)
            return e
