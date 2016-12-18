# -*- coding: utf-8 -*-
# ********************PyQt5相关模块导入********************
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class LaserQtImageWindow(QWidget):
    '''
        系统第四个窗口页面中的图像放大显示区域类
    '''
    def __init__(self, imageName):
        super(LaserQtImageWindow, self).__init__()
        self.imageName = imageName
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统")
        self.setWindowIcon(QIcon('LaserQt_Ui/logo.png'))
        self.get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        image = QImage("LaserQt_Temp/{}".format(self.imageName))
        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap.fromImage(image))

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.addWidget(imageLabel)

    def get_current_screen_size(self):
        self.width = int(444 * 1.2)
        self.height = int(436 * 1.2)
        