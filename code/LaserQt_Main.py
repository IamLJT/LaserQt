# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView 
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_Gui.LaserQt_Gui_Button import BrowseButton, NextButton, QuitButton, EditButton, UpdateButton
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
        self.first_page()

    def first_page(self):
        self.directoryLineEdit = QLineEdit()
        self.directoryLineEdit.setStyleSheet(
            '''
            QLineEdit {
                background-color: white;
            }
            '''
        )
        browseButton = BrowseButton()
        browseButton.clicked.connect(self.browse_directory)
        # 左半部分顶部布局
        self.leftTopLayout = QHBoxLayout()
        self.leftTopLayout.addWidget(self.directoryLineEdit)
        self.leftTopLayout.setSpacing(20)
        self.leftTopLayout.addWidget(browseButton)

        self.canvas = StaticCanvas()
        canvasRegionLable = QLabel("数据可视化区域")
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.addWidget(canvasRegionLable)
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvas)

        nextButton = NextButton()
        quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.addWidget(nextButton)
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addLayout(self.leftTopLayout)
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.setSpacing(60)
        self.leftLayout.addLayout(self.leftBottomLayout)

        tableRegionLable = QLabel("数据列表区域")
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
        self.rightMiddleLayout.addWidget(tableRegionLable)
        self.rightMiddleLayout.setSpacing(10)
        self.rightMiddleLayout.addWidget(self.dataTable)

        self.editButton = EditButton()
        self.editButton.clicked.connect(self.edit_the_table)
        updateButton = UpdateButton()
        updateButton.clicked.connect(self.update_the_plot)
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.addWidget(self.editButton)
        self.rightBottomLayout.setSpacing(60)
        self.rightBottomLayout.addWidget(updateButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.setSpacing(60)
        self.rightLayout.addLayout(self.rightBottomLayout )

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 38)
        self.widgetLayout.addLayout(self.leftLayout)
        self.widgetLayout.setSpacing(40)
        self.widgetLayout.addLayout(self.rightLayout) 

        self.setLayout(self.widgetLayout)

    def second_page():
        pass

    def third_page():
        pass

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
                newItem = QTableWidgetItem(str(value))
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
            if flag == 1.0:
                self.canvas.axes.plot([xStart, xEnd], [yStart, yEnd], 'r', label=u"正面加工路径")
            elif flag == 0.0:
                self.canvas.axes.plot([xStart, xEnd], [yStart, yEnd], 'b', label=u"反面加工路径")
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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myLaserQt = LaserQtMainWindow()
    myLaserQt.show()
    sys.exit(app.exec_())
