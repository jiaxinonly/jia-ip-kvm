# -*- coding: utf-8 -*-
# File: app.py
# Time: 2022/12/27 12:33
# Author: jiaxin
# Email: 1094630886@qq.com
import eventlet

eventlet.monkey_patch()
import base64
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from lib.HID import CH9329
import cv2
from lib.log import logger
from lib.config import Config
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.secret_key

socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')  # async_mode='eventlet'

NAMESPACE = '/ws'

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(id):
    return User.get_id(id)


@socketio.on('login', namespace=NAMESPACE)
def login(msg):
    if msg['username'] == Config.username and msg['password'] == Config.password:
        login_user(User(msg['username'], msg['password']))
        emit('login', True)
        logger.info(f"{msg['username']} 登录成功")
    else:
        emit('login', False)
        logger.info(f"{msg['username']} 登录失败")


@login_required
@socketio.on('logout', namespace=NAMESPACE)
def login():
    logout_user()
    return "success"


@socketio.on('connect', namespace=NAMESPACE)
def connect():
    logger.info("ws 已连接")


@socketio.on('disconnect', namespace=NAMESPACE)
def disconnect():
    logger.info("ws 已断开")
    global camera
    global ch9329
    global client_num
    if client_num > 0:
        client_num -= 1

    # 关闭设备
    if client_num == 0 and (ch9329 or camera):
        logger.info("等待10秒准备关闭")
        time.sleep(10)
        if client_num == 0 and (ch9329 or camera):
            logger.info("等待结束，关闭资源")
            if ch9329 or camera:
                ch9329.close()
                camera.release()

        else:
            logger.info("有新连接，退出关闭")


# 键盘消息处理
@socketio.on('keyMsg', namespace=NAMESPACE)
def key_msg(msg):
    logger.debug(f"keyMsg消息: {msg}")
    global ch9329
    ch9329.keyboard_down(msg)
    time.sleep(0.001)
    ch9329.keyboard_up()


# 鼠标消息处理
@socketio.on('mouseMsg', namespace=NAMESPACE)
def mouse_msg(msg):
    logger.debug(f"mouseMsg消息：{msg}")
    global ch9329
    ch9329.mouse_relative_move(msg['key'], msg['x'], msg['y'])
    if msg['key']:
        time.sleep(0.001)
        ch9329.mouse_relative_stop()


@socketio.on('frameMsg', namespace=NAMESPACE)
def frame_msg(msg):
    logger.debug(f"frameMsg消息：{msg}")
    global camera
    if msg.get("type", None) == "resolution":
        logger.info("设置分辨率：{} * {}".format(msg['height'], msg['width']))
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, msg['height'])
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, msg['width'])
    elif msg.get("type", None) == "fps":
        logger.info("设置fps：{}".format(msg['fps']))
        camera.set(cv2.CAP_PROP_FPS, msg['fps'])


# 视频消息处理
@socketio.on('videoMsg', namespace=NAMESPACE)
def video_msg():
    global client_num
    global camera
    global ch9329

    logger.info("video 已连接")

    if client_num == 0:
        # 启动后第一次访问 camera和ch9329 未初始化过，值为none时 或者 非第一次访问，设备未打开时
        if (not camera or not ch9329) or (camera and ch9329 and (not camera.isOpened() or not ch9329.is_open())):
            logger.info("启动设备")
            s = time.time()
            camera = cv2.VideoCapture(Config.video_index, cv2.CAP_DSHOW)
            camera.set(cv2.CAP_PROP_FPS, Config.video_fps)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.video_height)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.video_width)
            camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
            t = time.time()
            logger.info(f"启动耗时 {t - s} 秒")
            ch9329 = CH9329('COM3', 115200)

    client_num = client_num + 1
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
    client_num = 0
    camera = None
    ch9329 = None
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
