# -*- coding: utf-8 -*-
# ********************系统自带相关模块导入********************
import os
import time
# ********************PyQt5相关模块导入********************
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog
# ********************用户自定义相关模块导入********************
from LaserQt_MainWindow import LaserQtMainWindow
from LaserQt_SecondWindow import LaserQtSecondWindow
from LaserQt_ThirdWindow import LaserQtThirdWindow
from LaserQt_FourthWindow import LaserQtFourthWindow
from LaserQt_ImageWindow import LaserQtImageWindow
from LaserQt_Gui.LaserQt_Gui_Dialog import MessageDialog

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class OverLoadClassMethod(object):
    '''
        利用该类分别对LaserQt_MainWindow.py、LaserQt_SecondWindow.py、LaserQt_ThirdWindow.py、LaserQt_FourthWindow.py中的部分按钮动态得绑定回调函数
    '''
    def __init__(self):
        super(OverLoadClassMethod, self).__init__()
    
    # LaserQt_MainWindow.next_page方法
    def laser_qt_main_window_next_page(self):
        myLaserQtMainWindow.hide()  # 隐藏第一个窗口
        myLaserQtSecondWindow.show()  # 显示第二个窗口
    
    # LaserQt_MainWindow.prev_page方法
    def laser_qt_second_window_prev_page(self):
        myLaserQtSecondWindow.hide()
        myLaserQtMainWindow.show()

    # LaserQt_SecondWindow.next_page方法
    def laser_qt_second_window_next_page(self):
        myLaserQtSecondWindow.hide()
        myLaserQtThirdWindow.show()

    # LaserQt_SecondWindow.prev_page方法
    def laser_qt_third_window_prev_page(self):
        myLaserQtThirdWindow.hide()
        myLaserQtSecondWindow.show()

    # LaserQt_ThirdWindow.next_page方法
    def laser_qt_third_window_next_page(self):
        messageDialog = MessageDialog()
        reply = messageDialog.question(myLaserQtThirdWindow, "消息提示对话框", "您是否已完成点云数据处理？", messageDialog.Yes | messageDialog.No, messageDialog.Yes)
        # 在进入第四个窗口前，先提示用户是否完成点云数据处理，因为第四个窗口的绘图数据依赖于第三个窗口所操作处理的数据
        if reply == messageDialog.No:
            return
        
        myLaserQtThirdWindow.hide()
        myLaserQtFourthWindow.show()
        # 将第三个窗口操作处理所产生的中间数据赋给第三个窗口，减少重复计算
        myLaserQtFourthWindow.Z1 = myLaserQtThirdWindow.Z1
        myLaserQtFourthWindow.Z2 = myLaserQtThirdWindow.Z2
        # 初始化第四个窗口的画布
        messageDialog = MessageDialog()
        reply = messageDialog.information(myLaserQtThirdWindow, "消息提示对话框", "可视化初始化！", messageDialog.Yes, messageDialog.Yes)
        if reply == messageDialog.Yes:
            myLaserQtFourthWindow.init_the_canvas()

    # LaserQt_FourthWindow.prev_page方法
    def laser_qt_fourth_window_prev_page(self):
        myLaserQtFourthWindow.hide()
        myLaserQtSecondWindow.show()

    # LaserQt_FourthWindow.enlarge_the_plot方法
    def laser_qt_fourth_window_enlarge_the_plot(self):
        global myLaserQtImageWindow
        # 提示用户输入所要放大显示的图像索引号
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
            # 用户自定义显示的图，必须先绘图，才能放大显示
            elif num == 6:
                if os.path.exists("LaserQt_Temp/between_two_arbitrary_point_error_curve.png"):
                    myLaserQtImageWindow = LaserQtImageWindow("between_two_arbitrary_point_error_curve.png")
                    myLaserQtImageWindow.show()
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

    # 汉化处理
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
    # 按钮绑定回调函数
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
