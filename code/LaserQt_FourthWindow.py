# -*- coding: utf-8 -*-
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_AuxiliaryFunction import get_current_screen_size
from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import *
from LaserQt_Gui.LaserQt_Gui_Dialog import *

import os
import shutil

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class LaserQtFourthWindow(QWidget):
    def __init__(self):
        super(LaserQtFourthWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统")
        self.setWindowIcon(QIcon('LaserQt_Ui/logo.png'))
        self.width, self.height = get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        self.canvas = Static3DCanvasForPointCloud() ## TODO
        canvasRegionLable = QLabel("点云拟合三维可视化")
        qFont = QFont()
        qFont.setPointSize(12)
        canvasRegionLable.setFont(qFont)
        # 左半部分中部布局
        leftMiddleLayout = QVBoxLayout()
        leftMiddleLayout.setSpacing(10)
        leftMiddleLayout.addWidget(canvasRegionLable)
        leftMiddleLayout.addWidget(self.canvas)

        self.prevButton = PreviousButton()
        quitButton = QuitButton()
        # 左半部分底部布局
        leftBottomLayout = QHBoxLayout()
        leftBottomLayout.addStretch()
        leftBottomLayout.setSpacing(60)
        leftBottomLayout.addWidget(self.prevButton)
        leftBottomLayout.addWidget(quitButton)

        # 左半部分布局
        leftLayout = QVBoxLayout()
        leftLayout.setSpacing(23)
        leftLayout.addLayout(leftMiddleLayout)
        leftLayout.addLayout(leftBottomLayout)

        tableRegionLable = QLabel("误差曲线显示区域")
        tableRegionLable.setFont(qFont)
        self.canvas01 = StaticCanvasForErrorCurve01()
        self.canvas02 = StaticCanvasForErrorCurve02()
        self.canvas03 = StaticCanvasForErrorCurve03()
        self.canvas04 = StaticCanvasForErrorCurve04()
        self.canvas05 = StaticCanvasForErrorCurve05()
        self.canvas06 = StaticCanvasForErrorCurve06()
        dataShowLayout = QGridLayout()
        dataShowLayout.setHorizontalSpacing(2)
        dataShowLayout.setVerticalSpacing(2)
        dataShowLayout.addWidget(self.canvas01, 0, 0)
        dataShowLayout.addWidget(self.canvas02, 0, 1)
        dataShowLayout.addWidget(self.canvas03, 0, 2)
        dataShowLayout.addWidget(self.canvas04, 1, 0)
        dataShowLayout.addWidget(self.canvas05, 1, 1)
        dataShowLayout.addWidget(self.canvas06, 1, 2)
        # 右半部分顶部布局
        rightTopLayout = QVBoxLayout()
        rightTopLayout.addWidget(tableRegionLable)
        rightTopLayout.addLayout(dataShowLayout)

        XStartLable = QLabel("起点X坐标")
        XStartLable.setFont(qFont)
        self.XStartLineEdit = QLineEdit()
        YStartLable = QLabel("起点Y坐标")
        YStartLable.setFont(qFont)
        self.YStartLineEdit = QLineEdit()
        XEndLable = QLabel("终点X坐标")
        XEndLable.setFont(qFont)
        self.XEndLineEdit = QLineEdit()
        YEndLable = QLabel("终点Y坐标")
        YEndLable.setFont(qFont)
        self.YEndLineEdit = QLineEdit()
        # 右半部分中部布局
        rightMiddleLayout = QGridLayout()
        rightMiddleLayout.addWidget(XStartLable, 0, 0)
        rightMiddleLayout.addWidget(self.XStartLineEdit, 0, 1)
        rightMiddleLayout.addWidget(YStartLable, 0, 2)
        rightMiddleLayout.addWidget(self.YStartLineEdit, 0, 3)
        rightMiddleLayout.addWidget(XEndLable, 1, 0)
        rightMiddleLayout.addWidget(self.XEndLineEdit, 1, 1)
        rightMiddleLayout.addWidget(YEndLable, 1, 2)
        rightMiddleLayout.addWidget(self.YEndLineEdit, 1, 3)
        
        confirmButton = ConfirmButton()
        confirmButton.clicked.connect(self.between_two_arbitrary_point_error_curve)
        self.enlargeButton = EnlargeButton()
        # 右半部分底部布局
        rightBottomLayout = QHBoxLayout()
        rightBottomLayout.addStretch()
        rightBottomLayout.setSpacing(60)
        rightBottomLayout.addWidget(confirmButton)
        rightBottomLayout.addWidget(self.enlargeButton)

        # 右半部分布局
        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(30)
        rightLayout.addLayout(rightTopLayout)
        rightLayout.addLayout(rightMiddleLayout)
        rightLayout.addLayout(rightBottomLayout)

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.setSpacing(20)
        self.widgetLayout.addLayout(leftLayout)
        self.widgetLayout.addLayout(rightLayout)

    # 类方法重载 -- 关闭窗口事件
    def closeEvent(self, event):
        messageDialog = MessageDialog()
        reply = messageDialog.question(self, "消息提示对话框", "您要退出系统吗?", messageDialog.Yes | messageDialog.No, messageDialog.No)
        if reply == messageDialog.Yes:
            event.accept()
        else:
            event.ignore()

    def init_the_canvas(self):
        self.canvas.axes.plot([0], [0])
        self.canvas.axes.hold(True)
        self.canvas.axes.set_xlim([0, 100])
        self.canvas.axes.set_xticks(np.arange(0, 101, 10))
        self.canvas.axes.set_ylim([0, 100])
        self.canvas.axes.set_yticks(np.arange(0, 101, 10))
        self.canvas.axes.set_zticks([])
        self.canvas.axes.set_xlabel("加工板水平方向", fontproperties=FONT, fontsize=9)
        self.canvas.axes.set_ylabel("加工板垂直方向", fontproperties=FONT, fontsize=9)
        self.canvas.axes.grid(True, which="both")

        X = []; Y = [];# X， Y的取值介于1～100？
        X = [[_] * 100 for _ in range(1, 101)] 
        Y = [_ for _ in range(1, 101)] * 100

        # myLaserQtSub02.Z1 和  myLaserQtSub02.Z2 哪个是被减数 哪个是减数
        self.canvas.axes.scatter(X, Y, self.Z1, c='red')
        self.canvas.axes.scatter(X, Y, self.Z2, c='black')

        self.canvas.draw()
        self.canvas.axes.hold(False)

        if os.path.exists("LaserQt_Temp"):
            shutil.rmtree("LaserQt_Temp")
        os.mkdir("LaserQt_Temp")
        
        self.horizontal_direction_1_3_error_curve()
        self.horizontal_direction_1_2_error_curve()
        self.horizontal_direction_2_3_error_curve()
        self.vertical_direction_1_3_error_curve()
        self.vertical_direction_2_3_error_curve() 
        
    def horizontal_direction_1_3_error_curve(self):
        from matplotlib.pyplot import savefig
        error = [] 
        for i in range(1, 101):
            error.append(self.Z1[100 * 32 + i] - self.Z2[100 * 32 + i])

        self.canvas01.axes.plot()
        self.canvas01.axes.hold(True)
        self.canvas01.axes.set_xlim([0, 100])
        self.canvas01.axes.set_xticks(np.arange(0, 101, 10))
        self.canvas01.axes.set_title("加工板水平方向1/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.canvas01.axes.grid(True, which="both")
        self.canvas01.axes.plot(range(1, 101), error, 'r')
        self.canvas01.print_figure("LaserQt_Temp/horizontal_direction_1_3_error_curve.png")
        self.canvas01.draw()
        self.canvas01.axes.hold(False)

    def horizontal_direction_1_2_error_curve(self):
        error = [] 
        for i in range(1, 101):
            error.append(self.Z1[100 * 49 + i] - self.Z2[100 * 49 + i])

        self.canvas02.axes.plot()
        self.canvas02.axes.hold(True)
        self.canvas02.axes.set_xlim([0, 100])
        self.canvas02.axes.set_xticks(np.arange(0, 101, 10))
        self.canvas02.axes.set_title("加工板水平方向1/2处误差曲线图", fontproperties=FONT, fontsize=14)
        self.canvas02.axes.grid(True, which="both")
        self.canvas02.axes.plot(range(1, 101), error, 'r')
        self.canvas02.print_figure("LaserQt_Temp/horizontal_direction_1_2_error_curve.png")
        self.canvas02.draw()
        self.canvas02.axes.hold(False)

    def horizontal_direction_2_3_error_curve(self):
        error = [] 
        for i in range(1, 101):
            error.append(self.Z1[100 * 65 + i] - self.Z2[100 * 65 + i])

        self.canvas03.axes.plot()
        self.canvas03.axes.hold(True)
        self.canvas03.axes.set_xlim([0, 100])
        self.canvas03.axes.set_xticks(np.arange(0, 101, 10))
        self.canvas03.axes.set_title("加工板水平方向2/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.canvas03.axes.grid(True, which="both")
        self.canvas03.axes.plot(range(1, 101), error, 'r')
        self.canvas03.print_figure("LaserQt_Temp/horizontal_direction_2_3_error_curve.png")
        self.canvas03.draw()
        self.canvas03.axes.hold(False)

    def vertical_direction_1_3_error_curve(self):
        error = [] 
        for i in range(100):
            error.append(self.Z1[100 * i + 33] - self.Z2[100 * i + 33])

        self.canvas04.axes.plot()
        self.canvas04.axes.hold(True)
        self.canvas04.axes.set_xlim([0, 100])
        self.canvas04.axes.set_xticks(np.arange(0, 101, 10))
        self.canvas04.axes.set_title("加工板垂直方向1/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.canvas04.axes.grid(True, which="both")
        self.canvas04.axes.plot(range(1, 101), error, 'r')
        self.canvas04.print_figure("LaserQt_Temp/vertical_direction_1_3_error_curve.png")
        self.canvas04.draw()
        self.canvas04.axes.hold(False)

    def vertical_direction_2_3_error_curve(self):
        error = [] 
        for i in range(100):
            error.append(self.Z1[100 * i + 66] - self.Z2[100 * i + 66])

        self.canvas05.axes.plot()
        self.canvas05.axes.hold(True)
        self.canvas05.axes.set_xlim([0, 100])
        self.canvas05.axes.set_xticks(np.arange(0, 101, 10))
        self.canvas05.axes.set_title("加工板垂直方向2/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.canvas05.axes.grid(True, which="both")
        self.canvas05.axes.plot(range(1, 101), error, 'r')
        self.canvas05.print_figure("LaserQt_Temp/vertical_direction_2_3_error_curve.png")
        self.canvas05.draw()
        self.canvas05.axes.hold(False)

    def between_two_arbitrary_point_error_curve(self):
        x1 = int(self.XStartLineEdit.text().strip())
        y1 = int(self.YStartLineEdit.text().strip())
        x2 = int(self.XEndLineEdit.text().strip())
        y2 = int(self.YEndLineEdit.text().strip())

        k = (y2 - y1) / (x2 -x1) # 两点连线的斜率

        dots_index = []

        if x1 < x2:
            if y1 < y2:
                while x1 <= x2 and y1 <= y2:
                    pass
            else:
                while x1 <= x2 and y1 >= y2:
                    pass
        else:
            if y1 < y2:
                while x1 <= x2 and y1 <= y2:
                    pass
            else:
                while x1 <= x2 and y1 >= y2:
                    pass
