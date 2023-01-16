# -*- coding: utf-8 -*-
# File: HID.py
# Time: 2022/12/29 18:37
# Author: jiaxin
# Email: 1094630886@qq.com
import abc
import serial
import time
import string


class HID:
    @abc.abstractmethod
    def __init__(self):
        pass

    def get_info(self):
        pass

    @abc.abstractmethod
    def keyboard_down(self, key):
        pass

    @abc.abstractmethod
    def keyboard_up(self, key=None):
        pass

    @abc.abstractmethod
    def mouse_absolute_move(self, key, x, y):
        pass

    @abc.abstractmethod
    def mouse_relative_move(self, key, x, y):
        pass


class CH9329(HID):
    # HEAD + ADDR + CMD + LEN
    KEYBOARD_HEAD = [0x57, 0xab, 0x00, 0x02, 0x08]
    MOUSE_HEAD = [0x57, 0xab, 0x00, 0x05, 0x05]

    KEYBOARD_TABLE = {'Enter': 0x28, 'Escape': 0x29, 'Backspace': 0x2a, 'Tab': 0x2b, ' ': 0x2c, '-': 0x2d, '=': 0x2e,
                      '[': 0x2f, ']': 0x30, '\\': 0x31, ';': 0x33, "'": 0x34, '`': 0x35, ',': 0x36, '.': 0x37,
                      '/': 0x38, 'CapsLock': 0x39, 'Insert': 0x49, 'Delete': 0x4c, 'ArrowRight': 0x4f,
                      'ArrowLeft': 0x50, 'ArrowDown': 0x51,
                      'ArrowUp': 0x52}

    KEYBOARD_CTRL = {
        'ControlLeft': 0,
        'ShiftLeft': 1,
        'AltLeft': 2,
        'MetaLeft': 3,  # windows按键
        'ControlRight': 4,
        'ShiftRight': 5,
        'AltRight': 6,
        'MetaRight': 7
    }

    MOUSE_KEY = {
        'LeftKey': 0,
        'RightKey': 1,
        'MiddleKey': 2
    }

    # 字母  A ASCII码 65
    for i in range(26):
        KEYBOARD_TABLE[chr(65 + i)] = 0x04 + i

    # 数字  0 ASCII码 48
    KEYBOARD_TABLE['0'] = 0x27
    for i in range(9):
        KEYBOARD_TABLE[chr(49 + i)] = 0x1e + i

    # F1~F12
    for i in range(1, 13):
        KEYBOARD_TABLE['F' + str(i)] = 0x3a - 1 + i

    def __init__(self, device, baudrate):
        self.hid_serial = serial.Serial(device, baudrate, timeout=1)
        pass

    def keyboard_down(self, key):
        package = []
        ctrl_key = 0x00

        normal_key = []
        for i in key.split('+'):
            if i in CH9329.KEYBOARD_CTRL:
                ctrl_key += 1 << CH9329.KEYBOARD_CTRL[i]
            else:
                normal_key.append(i)

        # 最多6键
        normal_key = normal_key[:6]

        package.append(ctrl_key)  # 第1个字节，控制键
        package.append(0x00)  # 第2个字节，固定值0x00

        for i in normal_key:
            if i in string.ascii_letters:
                i = i.upper()
            package.append(CH9329.KEYBOARD_TABLE[i])

        for i in range(6 - len(normal_key)):
            package.append(0x00)

        package = CH9329.KEYBOARD_HEAD + package

        # 求和并对溢出进行&操作 272 & 0xff = 16  0xff即255 满255归0 272-255-1=16
        package.append(sum(package) & 0xFF)
        self.hid_serial.write(bytes(package))
        # 忽略回复消息
        self.hid_serial.flushInput()

    def keyboard_up(self, key=None):
        package = CH9329.KEYBOARD_HEAD + [0x00] * 8
        package.append(sum(package) & 0xff)
        self.hid_serial.write(bytes(package))
        self.hid_serial.flushInput()

    def mouse_absolute_move(self, key, x, y):
        pass

    def mouse_relative_move(self, key, x, y):
        package = []

        package.append(0x01)  # 第1个字节，固定值0x01

        mouse_key = 0x00

        if key is None:
            # 第2个字节 鼠标按键
            package.append(0x00)

            # 第3、4个字节 x 和 y
            # print(x, y)
            for i in x, y:
                if i == 0:
                    package.append(0x00)
                elif i > 0:
                    if i > 0x7f:
                        # print(i, 0x7f)
                        package.append(0x7f)
                    else:
                        # print(i)
                        package.append(i)
                elif i < 0:
                    if i < -0x7f:
                        # print(0x81)
                        package.append(0x81)
                    else:
                        # print(0x100 + i)
                        package.append(0x100 + i)

        else:
            # 第2个字节 鼠标按键
            mouse_key += 1 << CH9329.MOUSE_KEY[key]
            package.append(mouse_key)
            # 第3、4个字节， x y 都为零
            package.append(0x00)
            package.append(0x00)

        # 第5个字节 滚动
        package.append(0x00)

        package = CH9329.MOUSE_HEAD + package

        # 求和并对溢出进行&操作 272 & 0xff = 16  0xff即255 满255归0 272-255-1=16
        package.append(sum(package) & 0xFF)

        # print(package)
        self.hid_serial.write(bytes(package))
        # 忽略回复消息
        self.hid_serial.flushInput()

    def mouse_relative_stop(self):
        package = CH9329.MOUSE_HEAD + [0x00] * 5
        package.append(sum(package) & 0xff)
        self.hid_serial.write(bytes(package))
        self.hid_serial.flushInput()

    def is_open(self):
        return self.hid_serial.is_open

    def close(self):
        self.hid_serial.close()


if __name__ == '__main__':
    ch9329 = CH9329('COM5', 9600)
    # ch9329.keyboard_down('K')
    # time.sleep(0.001)
    # ch9329.keyboard_up()
