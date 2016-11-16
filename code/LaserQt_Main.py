# -*- coding: utf-8 -*-
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog

from LaserQt_MainWindow import LaserQtMainWindow
from LaserQt_SecondWindow import LaserQtSecondWindow
from LaserQt_ThirdWindow import LaserQtThirdWindow
from LaserQt_FourthWindow import LaserQtFourthWindow
from LaserQt_ImageWindow import LaserQtImageWindow

from LaserQt_Gui.LaserQt_Gui_Dialog import MessageDialog

import os

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class OverLoadClassMethod(object):
    def __init__(self):
        super(OverLoadClassMethod, self).__init__()

    def laser_qt_main_window_next_page(self):
        myLaserQtMainWindow.hide()
        myLaserQtSecondWindow.show()

    def laser_qt_second_window_prev_page(self):
        myLaserQtSecondWindow.hide()
        myLaserQtMainWindow.show()

    def laser_qt_second_window_next_page(self):
        myLaserQtSecondWindow.hide()
        myLaserQtThirdWindow.show()

    def laser_qt_third_window_prev_page(self):
        myLaserQtThirdWindow.hide()
        myLaserQtSecondWindow.show()

    def laser_qt_third_window_next_page(self):
        messageDialog = MessageDialog()
        reply = messageDialog.question(myLaserQtThirdWindow, "消息提示对话框", "您是否已完成点云数据处理？", messageDialog.Yes | messageDialog.No, messageDialog.Yes)
        if reply == messageDialog.No:
            return
        myLaserQtThirdWindow.hide()
        myLaserQtFourthWindow.show()
        myLaserQtFourthWindow.Z1 = myLaserQtThirdWindow.Z1
        myLaserQtFourthWindow.Z2 = myLaserQtThirdWindow.Z2
        myLaserQtFourthWindow.init_the_canvas()

    def laser_qt_fourth_window_prev_page(self):
        myLaserQtFourthWindow.hide()
        myLaserQtSecondWindow.show()

    def laser_qt_fourth_window_enlarge_the_plot(self):
        global myLaserQtImageWindow
        num, isOk = QInputDialog.getInt(myLaserQtFourthWindow, "复杂曲率板加工系统", "输入待放大误差曲线图像序号", 1, 1, 6, 1)
        if isOk:
            if num == 1:
                myLaserQtImageWindow = LaserQtImageWindow("horizontal_direction_1_3_error_curve.png")
                myLaserQtImageWindow.show()
            elif num == 2:
                myLaserQtImageWindow = LaserQtImageWindow("horizontal_direction_1_2_error_curve.png")
                myLaserQtImageWindow.show()
            elif num == 3:
                myLaserQtImageWindow = LaserQtImageWindow("horizontal_direction_2_3_error_curve.png")
                myLaserQtImageWindow.show()
            elif num == 4:
                myLaserQtImageWindow = LaserQtImageWindow("vertical_direction_1_3_error_curve.png")
                myLaserQtImageWindow.show()
            elif num == 5:
                myLaserQtImageWindow = LaserQtImageWindow("vertical_direction_2_3_error_curve.png")
                myLaserQtImageWindow.show()
            elif num == 6:
                if os.path.exists("LaserQt_Temp/between_two_arbitrary_point_error_curve.png"):
                    myLaserQtImageWindow = LaserQtImageWindow("between_two_arbitrary_point_error_curve.png")
                    myLaserQtImageWindow.show
                else:
                    messageDialog = MessageDialog()
                    messageDialog.warning(myLaserQtFourthWindow, "消息提示对话框", "请先绘图！", messageDialog.Yes, messageDialog.Yes)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    # 读取样式表
    file = open("LaserQt_Gui/LaserQt_Gui_Style.qss", 'r')
    styleSheet = file.read()
    file.close()
    # 设置全局样式
    qApp.setStyleSheet(styleSheet)

    tran = QTranslator()
    tran.load("qt_zh_CN.qm", "LaserQt_Font/")
    qApp.installTranslator(tran)

    myLaserQtMainWindow = LaserQtMainWindow()
    myLaserQtSecondWindow = LaserQtSecondWindow()
    myLaserQtThirdWindow = LaserQtThirdWindow()
    myLaserQtFourthWindow  = LaserQtFourthWindow()
    myLaserQtImageWindow = None

    # 对实例方法进行动态修改
    overLoad = OverLoadClassMethod()

    myLaserQtMainWindow.next_page = overLoad.laser_qt_main_window_next_page
    myLaserQtMainWindow.nextButton.clicked.connect(myLaserQtMainWindow.next_page)

    myLaserQtSecondWindow.prev_page = overLoad.laser_qt_second_window_prev_page
    myLaserQtSecondWindow.prevButton.clicked.connect(myLaserQtSecondWindow.prev_page)
    myLaserQtSecondWindow.next_page = overLoad.laser_qt_second_window_next_page
    myLaserQtSecondWindow.nextButton.clicked.connect(myLaserQtSecondWindow.next_page)

    myLaserQtThirdWindow.prev_page = overLoad.laser_qt_third_window_prev_page
    myLaserQtThirdWindow.prevButton.clicked.connect(myLaserQtThirdWindow.prev_page)
    myLaserQtThirdWindow.next_page = overLoad.laser_qt_third_window_next_page
    myLaserQtThirdWindow.nextButton.clicked.connect(myLaserQtThirdWindow.next_page)

    myLaserQtFourthWindow.prev_page = overLoad.laser_qt_fourth_window_prev_page
    myLaserQtFourthWindow.prevButton.clicked.connect(myLaserQtFourthWindow.prev_page)
    myLaserQtFourthWindow.enlarge_the_plot = overLoad.laser_qt_fourth_window_enlarge_the_plot
    myLaserQtFourthWindow.enlargeButton.clicked.connect(myLaserQtFourthWindow.enlarge_the_plot)

    # 显示第一个主窗口
    myLaserQtMainWindow.show()
    sys.exit(app.exec_())
