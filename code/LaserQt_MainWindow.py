# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtWidgets import QWidget

from LaserQt_AuxiliaryFunction import check_os, get_current_screen_size
from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import *
from LaserQt_Gui.LaserQt_Gui_Dialog import *

import xlrd
import xlutils.copy as xlcopy

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class LaserQtMainWindow(QWidget):
    def __init__(self):
        super(LaserQtMainWindow, self).__init__()
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
        self.directoryLineEdit = QLineEdit()
        browseButton = BrowseButton()
        browseButton.clicked.connect(self.browse_directory)
        # 左半部分顶部布局
        leftTopLayout = QHBoxLayout()
        leftTopLayout.setSpacing(20)
        leftTopLayout.addWidget(self.directoryLineEdit)
        leftTopLayout.addWidget(browseButton)

        self.canvas = StaticCanvasForPathInfo()
        canvasRegionLable = QLabel("数据可视化区域")
        qFont = QFont()
        qFont.setPointSize(12)
        canvasRegionLable.setFont(qFont)
        # 左半部分中部布局
        leftMiddleLayout = QVBoxLayout()
        leftMiddleLayout.setSpacing(10)
        leftMiddleLayout.addWidget(canvasRegionLable)
        leftMiddleLayout.addWidget(self.canvas)

        self.nextButton = NextButton()
        quitButton = QuitButton()
        # 左半部分底部布局
        leftBottomLayout = QHBoxLayout()
        leftBottomLayout.addStretch()
        leftBottomLayout.setSpacing(60)
        leftBottomLayout.addWidget(self.nextButton)
        leftBottomLayout.addWidget(quitButton)

        # 左半部分布局
        leftLayout = QVBoxLayout()
        leftLayout.setSpacing(18)
        leftLayout.addLayout(leftTopLayout)
        leftLayout.addLayout(leftMiddleLayout)
        leftLayout.addLayout(leftBottomLayout)

        tableRegionLable = QLabel("数据列表区域")
        tableRegionLable.setFont(qFont)
        self.dataTable = QTableWidget(0, 7)
        self.dataTable.setHorizontalHeaderLabels(["起点X坐标", "起点Y坐标", "终点X坐标", "终点Y坐标", "下压量", "热参数", "正反标志"])
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 按照表格宽度对各单元格宽度进行均分
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 禁止编辑单元格
        self.editFlag = False
        # 右半部分中部布局
        rightMiddleLayout = QVBoxLayout()
        rightMiddleLayout.setSpacing(10)
        rightMiddleLayout.addWidget(tableRegionLable)
        rightMiddleLayout.addWidget(self.dataTable)

        self.editButton = EditButton()
        self.editButton.clicked.connect(self.edit_the_table)
        updateButton = UpdateButton()
        updateButton.clicked.connect(self.update_the_plot)
        # 右半部分底部布局
        rightBottomLayout = QHBoxLayout()
        rightBottomLayout.addStretch()
        rightBottomLayout.setSpacing(60)
        rightBottomLayout.addWidget(self.editButton)
        rightBottomLayout.addWidget(updateButton)

        # 右半部分布局
        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(18)
        rightLayout.addLayout(rightMiddleLayout)
        rightLayout.addLayout(rightBottomLayout)

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.setSpacing(40)
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

    # 浏览本地文件夹中的文件并选择文件
    def browse_directory(self):
        mainDirectory = check_os()
        currentFileDialog = OpenFileDialog()
        fileName, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Excel Files (*.xlsx)")
        if fileName != "":
            self.fileName = fileName
            self.directoryLineEdit.setText(self.fileName)
            self.put_the_data_into_table()
            self.plot_the_data()
    
    # 读取Excel文件数据进表格
    def put_the_data_into_table(self):
        excelReadOnly = xlrd.open_workbook(self.fileName)
        table = excelReadOnly.sheets()[0]
        self.numOfPath = numOfRows = table.nrows
        rowIndex = self.dataTable.rowCount()  # 获取当前表格的行数，默认为0行
        self.dataTable.setRowCount(rowIndex + numOfRows)  # 根据Excel文件的行数动态得设置表格的行数
        self.numofParams = numOfColums = table.ncols
        for i in range(numOfRows):
            for j in range(numOfColums):
                value = table.cell(i, j).value
                ## TODO
                if j <= 3:
                    value = "%.2f"%value
                elif j > 3 and j <=5:
                    value = "%.1f"%value
                elif j == 6:
                    value = "%d"%value
                newItem = QTableWidgetItem(value)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
                self.dataTable.setItem(i, j, newItem)
        messageDialog = MessageDialog()
        messageDialog.information(self, "消息提示对话框", "路径文件数据已读取！", messageDialog.Yes, messageDialog.Yes)

    # 绘制路径图
    def plot_the_data(self):
        self.canvas.axes.plot() # 很关键的代码！！！重新导入文件时清除所有的绘图
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
            if i == 0 :
                continue
            else:
                if label == labels[i - 1]:
                    continue
                else:
                    unique_handles.append(handles[i]); unique_handles.append(handles[i - 1])
                    unique_labels.append(labels[i]); unique_labels.append(labels[i - 1])
                    break
        self.canvas.axes.set_xlim([0, 2])
        self.canvas.axes.set_xticks(np.arange(0, 22, 2)/10)
        self.canvas.axes.set_ylim([0, 1])
        self.canvas.axes.set_yticks(np.arange(0, 11)/10)
        self.canvas.axes.set_title("加工路径静态图", fontproperties=FONT, fontsize=14)
        self.canvas.axes.set_xlabel("X - 板长方向（m）", fontproperties=FONT, fontsize=9)
        self.canvas.axes.set_ylabel("Y - 板宽方向（m）", fontproperties=FONT, fontsize=9)
        self.canvas.axes.legend(unique_handles, unique_labels, prop=FONT, bbox_to_anchor=(1.1, 1.1))
        self.canvas.axes.grid(True, which="both")
        self.canvas.draw()
        self.canvas.axes.hold(False)

    # 编辑表格
    def edit_the_table(self):
        if self.editFlag == False:
            self.editFlag = True
            self.editButton.setIcon(QIcon("LaserQt_Ui/forbidden.png"))
            self.editButton.setToolTip("禁止编辑")
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示对话框", "您已开启编辑表格功能！", messageDialog.Yes, messageDialog.Yes)
            self.dataTable.setEditTriggers(QAbstractItemView.CurrentChanged) # 允许编辑单元格

        else:
            self.editFlag = False
            self.editButton.setIcon(QIcon("LaserQt_Ui/edit.png"))
            self.editButton.setToolTip("开启编辑")
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示对话框", "您已关闭编辑表格功能！", messageDialog.Yes, messageDialog.Yes)
            self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 禁止编辑编辑单元格

    # 更新路径图
    def update_the_plot(self):
        self.plot_the_data()
        self.update_the_excel()
        messageDialog = MessageDialog()
        messageDialog.information(self, "消息提示对话框", "更新数据完毕！", messageDialog.Yes, messageDialog.Yes)

    def update_the_excel(self):
        excelReadOnly = xlrd.open_workbook(self.fileName)
        excelReadWrite = xlcopy.copy(excelReadOnly)
        sheet = excelReadWrite.get_sheet(0)
        for i in range(self.numOfPath):
            for j in range(self.numofParams):
                if j <= 3:
                    sheet.write(i, j, float(self.dataTable.item(i, j).text()))
                elif j > 3 and j <=5:
                    sheet.write(i, j, float(self.dataTable.item(i, j).text()))
                elif j == 6:
                    sheet.write(i, j, int(self.dataTable.item(i, j).text())) 
        excelReadWrite.save(self.fileName)
        