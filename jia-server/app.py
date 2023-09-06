# -*- coding: utf-8 -*-
# File: app.py
# Time: 2022/12/27 12:33
# Author: jiaxin
# Email: 1094630886@qq.com
import base64
import time

import flask
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from lib.HID import CH9329
import cv2
import eventlet
from lib.log import logger

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bPIaytvh7I12CY4x'

socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')  # async_mode='eventlet'

NAMESPACE = '/ws'

client_num = 0
camera = None
ch9329 = None


# s = time.time()

# camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# camera.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

# t = time.time()
# print(t - s)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@socketio.on('connect', namespace=NAMESPACE)
def connect(msg):
    global client_num
    global camera
    global ch9329

    logger.info("ws连接")

    if client_num == 0:
        # 启动后第一次访问 camera和ch9329 未初始化过，值为none时 或者 非第一次访问，设备未打开时
        if (not camera or not ch9329) or (camera and ch9329 and (not camera.isOpened() or not ch9329.is_open())):
            print("启动设备")
            s = time.time()
            camera = cv2.VideoCapture(0)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            camera.set(cv2.CAP_PROP_FPS, 60)
            camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
            t = time.time()
            print(t - s)
            ch9329 = CH9329('COM5', 115200)

    client_num = client_num + 1
    print(client_num)


@socketio.on('disconnect', namespace=NAMESPACE)
def disconnect():
    print("ws 断开")
    global client_num
    client_num = client_num - 1

    # 关闭设备
    if client_num == 0:
        print("等待10秒准备关闭")
        time.sleep(10)
        if client_num == 0:
            print("等待结束，关闭资源")
            ch9329.close()
            camera.release()

        else:
            print("有新连接，退出关闭")

    print(client_num)


# 键盘消息处理
@socketio.on('keyMsg', namespace=NAMESPACE)
def key_msg(msg):
    print(msg)
    ch9329.keyboard_down(msg)
    time.sleep(0.001)
    ch9329.keyboard_up()


# 鼠标消息处理
@socketio.on('mouseMsg', namespace=NAMESPACE)
def mouse_msg(msg: dict):
    # logger.debug(msg)
    ch9329.mouse_relative_move(msg['key'], msg['x'], msg['y'])
    if msg['key']:
        time.sleep(0.001)
        ch9329.mouse_relative_stop()


# 视频消息处理
@socketio.on('videoMsg', namespace=NAMESPACE)
def video_msg(msg):
    print(msg)
    #
    while True:
        # 一帧帧循环读取摄像头的数据
        success, frame = camera.read()
        if not success:
            break
        else:
            # 将每一帧的数据进行编码压缩，存放在memory中
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            img = base64.b64encode(frame).decode()
            emit('videoMsg', 'data:image/jpg;base64,' + img)
            time.sleep(0.001)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
