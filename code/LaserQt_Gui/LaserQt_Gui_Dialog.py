# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.04
'''

class BaseDialog(QDialog):
    '''
    基类对话框
    '''
    def __init__(self):
        super(BaseDialog, self).__init__()
    