# -*- coding: utf-8 -*-
# ********************系统自带相关模块导入********************
import platform
import time

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

# 检查当前操作系统版本信息并依此设置主路径
def check_os():
    if platform.system() == "Windows":
        return "D:/LaserQt-master/code/LaserQt_Material"
    elif platform.system() == "Linux":
        import getpass
        user = getpass.getuser()
        return "/home/" + user + "/"

# 返回当前操作系统版本信息
def return_os():
    if platform.system() == "Windows":
        return "Windows"
    elif platform.system() == "Linux":
        return "Linux"

# 获取当前屏幕尺寸
def get_current_screen_size():
    width = 1280
    height = 640
    return (width, height)

# 获取当前系统时间
def get_current_screen_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
