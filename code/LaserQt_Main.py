# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import FONT, StaticCanvas
from LaserQt_Gui.LaserQt_Gui_Dialog import OpenFileDialog
from LaserQt_Gui.LaserQt_Gui_Style import *

import xlrd, xlwt

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.07
'''

class LaserQtMainWindow(QWidget):
    def __init__(self):
        super(LaserQtMainWindow, self).__init__()
        self.setStyleSheet(
            '''
            QWidget {
                color: black;
                background-color: #DDDDDD;
            }
            '''
        )
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统-开发者V1.0版")
        self.get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        self.directoryLineEdit = QLineEdit()
        self.directoryLineEdit.setStyleSheet(
            '''
            QLineEdit {
                background-color: white;
            }
            '''
        )
        self.browseButton = BrowseButton()
        self.browseButton.clicked.connect(self.browse_directory)
        # 左半部分顶部布局
        self.leftTopLayout = QHBoxLayout()
        self.leftTopLayout.addWidget(self.directoryLineEdit)
        self.leftTopLayout.setSpacing(20)
        self.leftTopLayout.addWidget(self.browseButton)

        self.canvas = StaticCanvas()
        self.canvasRegionLable = QLabel("数据可视化区域")
        self.qFont = QFont()
        self.qFont.setPointSize(14)
        self.canvasRegionLable.setFont(self.qFont)
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.addWidget(self.canvasRegionLable)
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvas)

        self.nextButton = NextButton()
        self.nextButton.clicked.connect(self.next_page)
        self.quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.addWidget(self.nextButton)
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addLayout(self.leftTopLayout)
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.setSpacing(23)
        self.leftLayout.addLayout(self.leftBottomLayout)

        self.tableRegionLable = QLabel("数据列表区域")
        self.tableRegionLable.setFont(self.qFont)
        self.dataTable = QTableWidget(100, 7)
        self.dataTable.setStyleSheet(
            '''
            QTableWidget {
                background-color: white;
            }
            '''
        )  
        self.dataTable.setHorizontalHeaderLabels(["起点X坐标", "起点Y坐标", "终点X坐标", "终点Y坐标", "下压量", "热参数", "正反标志"])
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 按照表格宽度对各单元格宽度进行均分
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 禁止编辑单元格
        self.editFlag = False
        # 右半部分中部布局
        self.rightMiddleLayout = QVBoxLayout()
        self.rightMiddleLayout.addWidget(self.tableRegionLable)
        self.rightMiddleLayout.setSpacing(10)
        self.rightMiddleLayout.addWidget(self.dataTable)

        self.editButton = EditButton()
        self.editButton.clicked.connect(self.edit_the_table)
        self.updateButton = UpdateButton()
        self.updateButton.clicked.connect(self.update_the_plot)
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.addWidget(self.editButton)
        self.rightBottomLayout.setSpacing(60)
        self.rightBottomLayout.addWidget(self.updateButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.setSpacing(23)
        self.rightLayout.addLayout(self.rightBottomLayout )

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.addLayout(self.leftLayout)
        self.widgetLayout.setSpacing(40)
        self.widgetLayout.addLayout(self.rightLayout)

    def get_current_screen_size(self):
        self.width = 1440
        self.height = 720

    # 类方法重载 -- 关闭窗口事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "消息提示对话框", "您要退出系统吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 浏览本地文件夹中的文件并选择文件
    def browse_directory(self):
        mainDirectory = self.check_os()
        currentFileDialog = OpenFileDialog()
        fileName, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Excel Files (*.xlsx)")
        self.directoryLineEdit.setText(fileName)
        if fileName != "":
            self.put_the_data_into_table(fileName)
            self.plot_the_data()
    
    # 读取Excel文件数据进表格
    def put_the_data_into_table(self, fileName):
        data = xlrd.open_workbook(fileName)
        table = data.sheets()[0]
        self.numOfPath = numOfRows = table.nrows
        numOfColums = table.ncols
        for i in range(numOfRows):
            for j in range(numOfColums):
                value = table.cell(i, j).value
                if j <= 3:
                    value = "%.2f"%value
                elif j > 3 and j <=5:
                    value = "%.1f"%value
                elif j == 6:
                    value = "%d"%value
                newItem = QTableWidgetItem(value)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
                self.dataTable.setItem(i, j, newItem)
        QMessageBox.information(self, "消息提示对话框", "路径文件数据已读取！", QMessageBox.Yes, QMessageBox.Yes)

    # 绘制路径图
    def plot_the_data(self):
        self.canvas.axes.hold(True)
        for i in range(self.numOfPath):
            xStart = float(self.dataTable.item(i, 0).text()) ;yStart = float(self.dataTable.item(i, 1).text())
            xEnd = float(self.dataTable.item(i, 2).text()) ;yEnd = float(self.dataTable.item(i, 3).text())
            flag = float(self.dataTable.item(i, 6).text())
            if flag == 1:
                self.canvas.axes.plot([xStart, xEnd], [yStart, yEnd], 'r', label="正面加工路径")
            elif flag == 0:
                self.canvas.axes.plot([xStart, xEnd], [yStart, yEnd], 'b', label="反面加工路径")
            self.canvas.axes.annotate('a', xy=(xStart, yStart), xytext=(xStart, yStart), fontsize=8)
            self.canvas.axes.annotate('b', xy=(xEnd, yEnd), xytext=(xEnd, yEnd), fontsize=8)
            self.canvas.axes.annotate(str(i + 1), xy=((xStart + xEnd)/2, (yStart + yEnd)/2), xytext=((xStart + xEnd)/2, (yStart + yEnd)/2))
        handles, labels = self.canvas.axes.get_legend_handles_labels()
        unique_handles = []; unique_labels = []
        for i, label in enumerate(labels):
            if label == labels[i + 1]:
                continue
            else:
                unique_handles.append(handles[i]); unique_handles.append(handles[i + 1])
                unique_labels.append(labels[i]); unique_labels.append(labels[i + 1])
                break
        self.canvas.axes.legend(unique_handles, unique_labels, prop=FONT, bbox_to_anchor=(1.1, 1.1))
        self.canvas.draw()
        self.canvas.axes.hold(False)

    # 编辑表格
    def edit_the_table(self):
        if self.editFlag == False:
            self.editFlag = True
            self.editButton.setText("禁止编辑")
            QMessageBox.information(self, "消息提示对话框", "您已开启编辑表格功能！", QMessageBox.Yes, QMessageBox.Yes)
            self.dataTable.setEditTriggers(QAbstractItemView.CurrentChanged) # 允许编辑单元格

        else:
            self.editFlag = False
            self.editButton.setText("开启编辑")
            QMessageBox.information(self, "消息提示对话框", "您已关闭编辑表格功能！", QMessageBox.Yes, QMessageBox.Yes)
            self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 禁止编辑编辑单元格

    # 更新路径图
    def update_the_plot(self):
        self.canvas.axes.plot()
        self.plot_the_data()
        QMessageBox.information(self, "消息提示对话框", "更新路径完毕！", QMessageBox.Yes, QMessageBox.Yes)

    # 检查当前的操作系统并依此设置主路径
    def check_os(self):
        import platform
        if platform.system() == "Windows":
            return "C:/"

        elif platform.system() == "Linux":
            import getpass
            user = getpass.getuser()
            return "/home/" + user + "/"

    def next_page(self):
        myLaserQt.hide()
        myLaserQtSub01.show()


class LaserQtMainWindowSub01(QWidget):
    def __init__(self):
        super(LaserQtMainWindowSub01, self).__init__()
        self.setStyleSheet(
            '''
            QWidget {
                color: black;
                background-color: #DDDDDD;
            }
            '''
        )
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统-开发者V1.0版")
        self.get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        self.canvas = StaticCanvas()
        self.canvasRegionLable = QLabel("数据可视化区域")
        self.qFont = QFont()
        self.qFont.setPointSize(14)
        self.canvasRegionLable.setFont(self.qFont)
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.addWidget(self.canvasRegionLable)
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvas)

        self.prevButton = PreviousButton()
        self.prevButton.clicked.connect(self.prev_page)
        self.nextButton = NextButton()
        self.nextButton.clicked.connect(self.next_page)
        self.quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.addWidget(self.prevButton)
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.nextButton)
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.setSpacing(23)
        self.leftLayout.addLayout(self.leftBottomLayout)

        self.tableRegionLable = QLabel("数据实时显示区域")
        self.tableRegionLable.setFont(self.qFont)
        self.dataShowLayout = QGridLayout()

        self.dataShow01Lable = QLabel("路径编号")
        self.dataShow01Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow01Lable, 0, 0)
        self.dataShow01Edit = QLineEdit()
        self.dataShow01Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow01Edit, 0, 1)

        self.dataShow02Lable = QLabel("起点坐标")
        self.dataShow02Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow02Lable, 1, 0)
        self.dataShow02Edit = QLineEdit()
        self.dataShow02Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow02Edit, 1, 1)

        self.dataShow03Lable = QLabel("终点坐标")
        self.dataShow03Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow03Lable, 2, 0)
        self.dataShow03Edit = QLineEdit()
        self.dataShow03Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow03Edit, 2, 1)

        self.dataShow04Lable = QLabel("下压量")
        self.dataShow04Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow04Lable, 3, 0)
        self.dataShow04Edit = QLineEdit()
        self.dataShow04Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow04Edit, 3, 1)

        self.dataShow05Lable = QLabel("热参数")
        self.dataShow05Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow05Lable, 4, 0)
        self.dataShow05Edit = QLineEdit()
        self.dataShow05Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow05Edit, 4, 1)

        self.dataShow06Lable = QLabel("加工时间")
        self.dataShow06Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow06Lable, 5, 0)
        self.dataShow06Edit = QLineEdit()
        self.dataShow06Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow06Edit, 5, 1)
        # 右半部分中部布局
        self.rightMiddleLayout = QVBoxLayout()
        self.rightMiddleLayout.addStretch()
        self.rightMiddleLayout.addWidget(self.tableRegionLable)
        self.rightMiddleLayout.addLayout(self.dataShowLayout)
        
        self.startProcessingButton = StartProcessingButton()
        self.startProcessingButton.clicked.connect(self.start_processing)
        self.stopProcessingButton = StopProcessingButton()
        self.stopProcessingButton.clicked.connect(self.stop_processing)
        self.continueProcessingButton = ContinueProcessingButton()
        self.continueProcessingButton.clicked.connect(self.continue_processing)
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.addWidget(self.startProcessingButton)
        self.rightBottomLayout.setSpacing(60)
        self.rightBottomLayout.addWidget(self.stopProcessingButton)
        self.rightBottomLayout.setSpacing(60)
        self.rightBottomLayout.addWidget(self.continueProcessingButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.setSpacing(62)
        self.rightLayout.addLayout(self.rightBottomLayout )

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.addLayout(self.leftLayout)
        self.widgetLayout.setSpacing(40)
        self.widgetLayout.addLayout(self.rightLayout)

    def get_current_screen_size(self):
        self.width = 1440
        self.height = 720

    def prev_page(self):
        myLaserQtSub01.hide()
        myLaserQt.show()

    def next_page(self):
        pass

    def start_processing(self):
        pass

    def stop_processing(self):
        pass

    def continue_processing(self):
        pass


class LaserQtMainWindowSub02(QWidget):
    pass


class LaserQtMainWindowSub03(QWidget):
    pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myLaserQt = LaserQtMainWindow()
    myLaserQtSub01 = LaserQtMainWindowSub01()
    myLaserQtSub02 = LaserQtMainWindowSub02()
    myLaserQtSub03 = LaserQtMainWindowSub03()
    myLaserQt.show()
    sys.exit(app.exec_())
