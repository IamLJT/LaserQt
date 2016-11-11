# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTextEdit

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.05
'''

class BaseDialog(QDialog):
    '''
    基类对话框
    '''
    def __init__(self):
        super(BaseDialog, self).__init__()


class BaseFileDialog(QFileDialog):
    '''
    基类文件对话框
    '''
    def __init__(self):
        super(BaseFileDialog, self).__init__()


class OpenFileDialog(BaseFileDialog):
    '''
    选择文件对话框，继承自基类文件对话框
    '''
    def __init__(self):
        super(OpenFileDialog, self).__init__()

    # 打开文件选择对话框，选择本地数据文件
    def open_file(self, *args, **kwargs):
        return self.getOpenFileName(*args, **kwargs)


class MessageDialog(QMessageBox):
    '''
    消息对话框，继承自QMessageBox
    '''
    def __init__(self):
        super(MessageDialog, self).__init__()
