# -*- coding: utf-8 -*-
# @Time    : 2021/9/9 17:02
# @Author  : kanghe
# @Email   : 244783726@qq.com
# @File    : utils_ws.py


import time
from websocket import create_connection

"""
ws 接口连接
"""
url = 'ws://192.192.185.65:30735/sf/log/pod'


# socket 连接建立后要先向服务器发送一条数据
while True:  # 一直链接，直到连接上就退出循环
    time.sleep(2)
    try:
        ws = create_connection(url)
        # socket 连接建立后要先向服务器发送一条数据
        ws.send(
            '{"tenant":"admin","container":"ss-singletable-0","pod":"ss-singletable-5b9496c544-xfkmv","lineLimit":100}')
        # 连接建立就退出
        break
    except Exception as e:
        print('连接异常：', e)
        continue

# 连接之后，此循环用于才持续获取数据
while True:
    response1 = ws.recv()
    print(response1, "返回的数据")