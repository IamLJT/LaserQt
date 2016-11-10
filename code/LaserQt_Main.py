# -*- coding: utf-8 -*-
import queue
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import *
from LaserQt_Gui.LaserQt_Gui_Dialog import OpenFileDialog

import threading
import time

import xlrd
import xlutils.copy as xlcopy

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.10
'''

# 检查当前的操作系统并依此设置主路径
def check_os():
    import platform
    if platform.system() == "Windows":
        return "C:/"

    elif platform.system() == "Linux":
        import getpass
        user = getpass.getuser()
        return "/home/" + user + "/"


class LaserQtMainWindow(QWidget):
    def __init__(self):
        super(LaserQtMainWindow, self).__init__()
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
        self.browseButton = BrowseButton()
        self.browseButton.clicked.connect(self.browse_directory)
        # 左半部分顶部布局
        self.leftTopLayout = QHBoxLayout()
        self.leftTopLayout.setSpacing(20)
        self.leftTopLayout.addWidget(self.directoryLineEdit)
        self.leftTopLayout.addWidget(self.browseButton)

        self.canvas = StaticCanvasForPathInfo()
        self.canvasRegionLable = QLabel("数据可视化区域")
        self.qFont = QFont()
        self.qFont.setPointSize(12)
        self.canvasRegionLable.setFont(self.qFont)
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvasRegionLable)
        self.leftMiddleLayout.addWidget(self.canvas)

        self.nextButton = NextButton()
        self.nextButton.clicked.connect(self.next_page)
        self.quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.nextButton)
        self.leftBottomLayout.addWidget(self.quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(18)
        self.leftLayout.addLayout(self.leftTopLayout)
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.addLayout(self.leftBottomLayout)

        self.tableRegionLable = QLabel("数据列表区域")
        self.tableRegionLable.setFont(self.qFont)
        self.dataTable = QTableWidget(100, 7)
        self.dataTable.setHorizontalHeaderLabels(["起点X坐标", "起点Y坐标", "终点X坐标", "终点Y坐标", "下压量", "热参数", "正反标志"])
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 按照表格宽度对各单元格宽度进行均分
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # 禁止编辑单元格
        self.editFlag = False
        # 右半部分中部布局
        self.rightMiddleLayout = QVBoxLayout()
        self.rightMiddleLayout.setSpacing(10)
        self.rightMiddleLayout.addWidget(self.tableRegionLable)
        self.rightMiddleLayout.addWidget(self.dataTable)

        self.editButton = EditButton()
        self.editButton.clicked.connect(self.edit_the_table)
        self.updateButton = UpdateButton()
        self.updateButton.clicked.connect(self.update_the_plot)
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.setSpacing(60)
        self.rightBottomLayout.addWidget(self.editButton)
        self.rightBottomLayout.addWidget(self.updateButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setSpacing(18)
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.addLayout(self.rightBottomLayout )

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.setSpacing(40)
        self.widgetLayout.addLayout(self.leftLayout)     
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
        QMessageBox.information(self, "消息提示对话框", "路径文件数据已读取！", QMessageBox.Yes, QMessageBox.Yes)

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
        self.plot_the_data()
        self.update_the_excel()
        QMessageBox.information(self, "消息提示对话框", "更新数据完毕！", QMessageBox.Yes, QMessageBox.Yes)

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

    def next_page(self):
        myLaserQt.hide()
        myLaserQtSub01.show()


class LaserQtMainWindowSub01(QWidget):
    def __init__(self):
        super(LaserQtMainWindowSub01, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统-开发者V1.0版")
        self.get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        self.canvas = DynamicCanvasForPathInfo() ## TODO
        self.canvasRegionLable = QLabel("数据可视化区域")
        self.qFont = QFont()
        self.qFont.setPointSize(12)
        self.canvasRegionLable.setFont(self.qFont)
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvasRegionLable)
        self.leftMiddleLayout.addWidget(self.canvas)

        self.prevButton = PreviousButton()
        self.prevButton.clicked.connect(self.prev_page)
        self.nextButton = NextButton()
        self.nextButton.clicked.connect(self.next_page)
        self.quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.prevButton)
        self.leftBottomLayout.addWidget(self.nextButton)
        self.leftBottomLayout.addWidget(self.quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(23)
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.addLayout(self.leftBottomLayout)

        self.tableRegionLable = QLabel("数据实时显示区域")
        self.tableRegionLable.setFont(self.qFont)
        self.dataShowLayout = QGridLayout()

        self.dataShow01Lable = QLabel("加载文件")
        self.dataShow01Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow01Lable, 0, 0)
        self.dataShow01Edit = QLineEdit()
        self.dataShow01Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow01Edit, 0, 1)

        self.dataShow02Lable = QLabel("路径编号")
        self.dataShow02Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow02Lable, 1, 0)
        self.dataShow02Edit = QLineEdit()
        self.dataShow02Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow02Edit, 1, 1)

        self.dataShow03Lable = QLabel("起点坐标")
        self.dataShow03Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow03Lable, 2, 0)
        self.dataShow03Edit = QLineEdit()
        self.dataShow03Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow03Edit, 2, 1)

        self.dataShow04Lable = QLabel("终点坐标")
        self.dataShow04Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow04Lable, 3, 0)
        self.dataShow04Edit = QLineEdit()
        self.dataShow04Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow04Edit, 3, 1)

        self.dataShow05Lable = QLabel("下压量")
        self.dataShow05Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow05Lable, 4, 0)
        self.dataShow05Edit = QLineEdit()
        self.dataShow05Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow05Edit, 4, 1)

        self.dataShow06Lable = QLabel("热参数")
        self.dataShow06Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow06Lable, 5, 0)
        self.dataShow06Edit = QLineEdit()
        self.dataShow06Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow06Edit, 5, 1)

        self.dataShow07Lable = QLabel("加工时间")
        self.dataShow07Lable.setFont(self.qFont)
        self.dataShowLayout.addWidget(self.dataShow07Lable, 6, 0)
        self.dataShow07Edit = QLineEdit()
        self.dataShow07Edit.setEnabled(False)
        self.dataShowLayout.addWidget(self.dataShow07Edit, 6, 1)
        # 右半部分中部布局
        self.rightMiddleLayout = QVBoxLayout()
        self.rightMiddleLayout.setSpacing(52)
        self.rightMiddleLayout.addWidget(self.tableRegionLable)
        self.rightMiddleLayout.addLayout(self.dataShowLayout)
        
        self.startProcessingButton = StartProcessingButton()
        self.startProcessingButton.clicked.connect(self.start_processing)
        self.timer = QTimer() # 初始化定时器对象
        self.timer.timeout.connect(self.time_count)
        self.mplThread = threading.Thread(target=self.socket_communication) ## 初始化socket通信子线程
        self.mplThread.setDaemon(True)
        self.stopProcessingButton = StopProcessingButton()
        self.stopProcessingButton.clicked.connect(self.stop_processing)
        self.continueProcessingButton = ContinueProcessingButton()
        self.continueProcessingButton.clicked.connect(self.continue_processing)
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.setSpacing(62)
        self.rightBottomLayout.addWidget(self.startProcessingButton)
        self.rightBottomLayout.addWidget(self.stopProcessingButton)
        self.rightBottomLayout.addWidget(self.continueProcessingButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setSpacing(75)
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.addLayout(self.rightBottomLayout )

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.setSpacing(40)
        self.widgetLayout.addLayout(self.leftLayout)
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

    def prev_page(self):
        myLaserQtSub01.hide()
        myLaserQt.show()

    def next_page(self):
        myLaserQtSub01.hide()
        myLaserQtSub02.show()

    def init_task_queue(self):
        self.myTaskQueue = queue.Queue(maxsize=100) # 任务队列 -- 生产者-消费者模式

        excelReadOnly = xlrd.open_workbook(myLaserQt.fileName)
        table = excelReadOnly.sheets()[0]
        numOfRows = table.nrows
        numOfColums = table.ncols
        for i in range(numOfRows):
            dataCell = []
            dataCell.append(i + 1)
            for j in range(numOfColums):
                value = table.cell(i, j).value
                dataCell.append(value)
            self.myTaskQueue.put(dataCell)


    def start_processing(self):
        self.init_task_queue()

        self.isStop = False

        self.dataShow01Edit.setText(myLaserQt.fileName)

        self.time = "00：00：00"
        self.count = 0

        self.timer.start(1000) ## TODO

        self.canvas.axes.plot()
        self.canvas.axes.hold(True)
        self.canvas.axes.set_xlim([0, 2])
        self.canvas.axes.set_xticks(np.arange(0, 22, 2)/10)
        self.canvas.axes.set_ylim([0, 1])
        self.canvas.axes.set_yticks(np.arange(0, 11)/10)
        self.canvas.axes.set_title("加工路径动态图", fontproperties=FONT, fontsize=14)
        self.canvas.axes.set_xlabel("X - 板长方向（m）", fontproperties=FONT, fontsize=9)
        self.canvas.axes.set_ylabel("Y - 板宽方向（m）", fontproperties=FONT, fontsize=9)
        self.canvas.axes.grid(True, which="both")

        while (not self.isStop) and (not self.myTaskQueue.empty()):
            dataCell = self.myTaskQueue.get()
            self.dataShow02Edit.setText(str(dataCell[0]))
            self.dataShow03Edit.setText('( ' + str(dataCell[1]) + ', ' + str(dataCell[2]) + ' )')
            self.dataShow04Edit.setText('( ' + str(dataCell[3]) + ', ' + str(dataCell[4]) + ' )')
            self.dataShow05Edit.setText(str(dataCell[5]))
            self.dataShow06Edit.setText(str(dataCell[6]))
            self.dataShow07Edit.setText(self.time) # 时间显示好像有点不靠谱！！！
            self.plot_the_dynamic_data(dataCell)
            qApp.processEvents() # 强制刷新界面
            time.sleep(1)

        self.timer.stop()

        if self.myTaskQueue.empty() == True:
            self.canvas.axes.hold(False)
            QMessageBox.information(self, "消息提示对话框", "所有路径加工完毕！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, "消息提示对话框", "您已停止加工！", QMessageBox.Yes, QMessageBox.Yes)

    def stop_processing(self):
        self.isStop = True

    def continue_processing(self):
        QMessageBox.information(self, "消息提示对话框", "您将开始加工！", QMessageBox.Yes, QMessageBox.Yes)

        self.isStop = False

        self.timer.start(1000) ## TODO
        
        while (not self.isStop) and (not self.myTaskQueue.empty()):
            dataCell = self.myTaskQueue.get()
            self.dataShow02Edit.setText(str(dataCell[0]))
            self.dataShow03Edit.setText('( ' + str(dataCell[1]) + ', ' + str(dataCell[2]) + ' )')
            self.dataShow04Edit.setText('( ' + str(dataCell[3]) + ', ' + str(dataCell[4]) + ' )')
            self.dataShow05Edit.setText(str(dataCell[5]))
            self.dataShow06Edit.setText(str(dataCell[6]))
            self.dataShow07Edit.setText(self.time) # 时间显示好像有点不靠谱！！！
            self.plot_the_dynamic_data(dataCell)
            qApp.processEvents() # 强制刷新界面
            time.sleep(1)
        
        self.timer.stop()

        if self.myTaskQueue.empty() == True:
            self.canvas.axes.hold(False)
            QMessageBox.information(self, "消息提示对话框", "所有路径加工完毕！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, "消息提示对话框", "您已停止加工！", QMessageBox.Yes, QMessageBox.Yes)

    def socket_communication(self):
        host = "127.0.0.1"
        port = 7070
        addr = (host, port)
        bufferSize = 1024 
        
        while True:
            tcpClientSock = socket(AF_INET, SOCK_STREAM)
            tcpClientSock.connect(addr)

            sendData = input('>> ')
            if not sendData:
                break
            else:
                tcpClientSock.send("{}\r\n".format(sendData).encode("utf-8"))
            
            recvData = tcpClientSock.recv(bufferSize).decode("utf-8")
            if not recvData:
                break
            else:
                dataCell = recvData.strip().split(',')
                self.plot_the_dynamic_data(dataCell)
            
            tcpClientSock.close()

    # 计时器
    def time_count(self):
        self.count += 1
        m = self.count // 60 # Python3中的整除写法 -- // 
        s = self.count % 60
        if s < 10:
            self.time = "00：0{}：0{}".format(m, s)
        else:
            self.time = "00：0{}：{}".format(m, s)

    def plot_the_dynamic_data(self, dataCell):
        if dataCell[7] == 1:
            self.canvas.axes.plot([float(dataCell[1]), float(dataCell[3])], [float(dataCell[2]), float(dataCell[4])], 'r', label="正面加工路径")
        else:
            self.canvas.axes.plot([float(dataCell[1]), float(dataCell[3])], [float(dataCell[2]), float(dataCell[4])], 'b', label="反面加工路径")
        self.canvas.draw()


class LaserQtMainWindowSub02(QWidget):
    def __init__(self):
        super(LaserQtMainWindowSub02, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统-开发者V1.0版")
        self.get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        self.targetDataLable = QLabel("目标数据")
        self.qFont = QFont()
        self.qFont.setPointSize(12)
        self.targetDataLable.setFont(self.qFont)
        self.scanningDataLable = QLabel("扫描数据")
        self.scanningDataLable.setFont(self.qFont)
        self.targetDataDirectoryLineEdit = QLineEdit()
        self.scanningDataDirectoryLineEdit = QLineEdit()
        self.targetDataBrowseButton = BrowseButton()
        self.targetDataBrowseButton.clicked.connect(self.browse_target_data_directory)
        self.scanningDataBrowseButton = BrowseButton()
        self.scanningDataBrowseButton.clicked.connect(self.browse_scanning_data_directory)
        # 左半部分顶部布局
        self.leftTopLayout = QGridLayout()
        self.leftTopLayout.addWidget(self.targetDataLable, 0, 0)
        self.leftTopLayout.addWidget(self.scanningDataLable, 1, 0)
        self.leftTopLayout.addWidget(self.targetDataDirectoryLineEdit, 0, 1)
        self.leftTopLayout.addWidget(self.scanningDataDirectoryLineEdit, 1, 1)
        self.leftTopLayout.addWidget(self.targetDataBrowseButton, 0, 2)
        self.leftTopLayout.addWidget(self.scanningDataBrowseButton, 1, 2)
        
        self.canvas = StaticCanvasForPointCloud()
        self.canvasRegionLable = QLabel("数据可视化区域")
        self.canvasRegionLable.setFont(self.qFont)
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvasRegionLable)
        self.leftMiddleLayout.addWidget(self.canvas)

        self.prevButton = PreviousButton()
        self.prevButton.clicked.connect(self.prev_page)
        self.nextButton = NextButton()
        self.nextButton.clicked.connect(self.next_page)
        self.quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.prevButton)
        self.leftBottomLayout.addWidget(self.nextButton)
        self.leftBottomLayout.addWidget(self.quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(23)
        self.leftLayout.addLayout(self.leftTopLayout)
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.addLayout(self.leftBottomLayout)

        self.logRegionLable = QLabel("后台执行过程展示区域")
        self.logRegionLable.setFont(self.qFont)
        self.logTextEdit = QTextEdit()
        self.executeProgressBar = QProgressBar()
        self.executeProgressBar.setValue(10)
        # 右半部分中部布局
        self.rightMiddleLayout = QVBoxLayout()
        self.rightMiddleLayout.addWidget(self.logRegionLable)
        self.rightMiddleLayout.addWidget(self.logTextEdit)
        self.rightMiddleLayout.addWidget(self.executeProgressBar)

        self.pointCloudDataScanButton = PointCloudDataScanButton()
        self.pointCloudDataScanButton.clicked.connect(self.point_cloud_data_scan)
        self.pointCloudDataDenoisingButton = PointCloudDataDenoisingButton()
        self.pointCloudDataDenoisingButton.clicked.connect(self.point_cloud_data_denoising )
        self.pointCloudDataFittingButton = PointCloudDataFittingButton()
        self.pointCloudDataFittingButton.clicked.connect(self.point_cloud_data_fitting)
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.setSpacing(60)
        self.rightBottomLayout.addWidget(self.pointCloudDataScanButton)
        self.rightBottomLayout.addWidget(self.pointCloudDataDenoisingButton)
        self.rightBottomLayout.addWidget(self.pointCloudDataFittingButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setSpacing(23)
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.addLayout(self.rightBottomLayout)

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.setSpacing(40)
        self.widgetLayout.addLayout(self.leftLayout)
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

    def prev_page(self):
        myLaserQtSub02.hide()
        myLaserQtSub01.show()

    def next_page(self):
        myLaserQtSub02.hide()
        myLaserQtSub03.show()

    def browse_target_data_directory(self): ## TODO
        mainDirectory = check_os()
        currentFileDialog = OpenFileDialog()
        fileName, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Text Files (*.txt)")
        if fileName != "":
            self.fileName = fileName
            self.targetDataDirectoryLineEdit.setText(self.fileName)

    def browse_scanning_data_directory(self): ## TODO
        mainDirectory = check_os()
        currentFileDialog = OpenFileDialog()
        fileName, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Text Files (*.txt)")
        if fileName != "":
            self.fileName = fileName
            self.scanningDataDirectoryLineEdit.setText(self.fileName)

    def point_cloud_data_scan(self):
        pass

    def point_cloud_data_denoising(self):
        pass

    def point_cloud_data_fitting(self):
        pass

class LaserQtMainWindowSub03(QWidget):
    def __init__(self):
        super(LaserQtMainWindowSub03, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统-开发者V1.0版")
        self.get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        self.canvas = StaticCanvasForPointCloud() ## TODO
        self.canvasRegionLable = QLabel("数据可视化区域")
        self.qFont = QFont()
        self.qFont.setPointSize(12)
        self.canvasRegionLable.setFont(self.qFont)
        # 左半部分中部布局
        self.leftMiddleLayout = QVBoxLayout()
        self.leftMiddleLayout.setSpacing(10)
        self.leftMiddleLayout.addWidget(self.canvasRegionLable)
        self.leftMiddleLayout.addWidget(self.canvas)

        self.prevButton = PreviousButton()
        self.prevButton.clicked.connect(self.prev_page)
        self.quitButton = QuitButton()
        # 左半部分底部布局
        self.leftBottomLayout = QHBoxLayout()
        self.leftBottomLayout.addStretch()
        self.leftBottomLayout.setSpacing(60)
        self.leftBottomLayout.addWidget(self.prevButton)
        self.leftBottomLayout.addWidget(self.quitButton)

        # 左半部分布局
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(23)
        self.leftLayout.addLayout(self.leftMiddleLayout)
        self.leftLayout.addLayout(self.leftBottomLayout)

        self.tableRegionLable = QLabel("误差曲线显示区域")
        self.tableRegionLable.setFont(self.qFont)

        self.canvas01 = StaticCanvasForErrorCurve01()
        self.canvas02 = StaticCanvasForErrorCurve02()
        self.canvas03 = StaticCanvasForErrorCurve03()
        self.canvas04 = StaticCanvasForErrorCurve04()
        self.canvas05 = StaticCanvasForErrorCurve05()
        self.canvas06 = StaticCanvasForErrorCurve06()
        self.dataShowLayout = QGridLayout()
        self.dataShowLayout.addWidget(self.canvas01, 0, 0)
        self.dataShowLayout.addWidget(self.canvas02, 0, 1)
        self.dataShowLayout.addWidget(self.canvas03, 0, 2)
        self.dataShowLayout.addWidget(self.canvas04, 1, 0)
        self.dataShowLayout.addWidget(self.canvas05, 1, 1)
        self.dataShowLayout.addWidget(self.canvas06, 1, 2)
        # 右半部分顶部布局
        self.rightTopLayout = QVBoxLayout()
        self.rightTopLayout.addWidget(self.tableRegionLable)
        self.rightTopLayout.addLayout(self.dataShowLayout)

        self.XStartLable = QLabel("起点X坐标")
        self.XStartLable.setFont(self.qFont)
        self.XStartLineEdit = QLineEdit()
        self.YStartLable = QLabel("起点Y坐标")
        self.YStartLable.setFont(self.qFont)
        self.YStartLineEdit = QLineEdit()
        self.XEndLable = QLabel("终点X坐标")
        self.XEndLable.setFont(self.qFont)
        self.XEndLineEdit = QLineEdit()
        self.YEndLable = QLabel("终点Y坐标")
        self.YEndLable.setFont(self.qFont)
        self.YEndLineEdit = QLineEdit()
        # 右半部分中部布局
        self.rightMiddleLayout = QGridLayout()
        self.rightMiddleLayout.addWidget(self.XStartLable, 0, 0)
        self.rightMiddleLayout.addWidget(self.XStartLineEdit, 0, 1)
        self.rightMiddleLayout.addWidget(self.YStartLable, 0, 2)
        self.rightMiddleLayout.addWidget(self.YStartLineEdit, 0, 3)
        self.rightMiddleLayout.addWidget(self.XEndLable, 1, 0)
        self.rightMiddleLayout.addWidget(self.XEndLineEdit, 1, 1)
        self.rightMiddleLayout.addWidget(self.YEndLable, 1, 2)
        self.rightMiddleLayout.addWidget(self.YEndLineEdit, 1, 3)
        
        self.confirmButton = ConfirmButton()
        # 右半部分底部布局
        self.rightBottomLayout = QHBoxLayout()
        self.rightBottomLayout.addStretch()
        self.rightBottomLayout.addWidget(self.confirmButton)

        # 右半部分布局
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setSpacing(30)
        self.rightLayout.addLayout(self.rightTopLayout)
        self.rightLayout.addLayout(self.rightMiddleLayout)
        self.rightLayout.addLayout(self.rightBottomLayout )

        # 全局布局
        self.widgetLayout = QHBoxLayout()
        self.widgetLayout.setContentsMargins(40, 40, 40, 40)
        self.widgetLayout.setSpacing(20)
        self.widgetLayout.addLayout(self.leftLayout)
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

    def prev_page(self):
        myLaserQtSub03.hide()
        myLaserQtSub01.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    # 读取样式表
    file = open("LaserQt_Gui/LaserQt_Gui_Style.qss", 'r')
    styleSheet = file.read()
    file.close()
    # 设置全局样式
    qApp.setStyleSheet(styleSheet)

    myLaserQt = LaserQtMainWindow()
    myLaserQtSub01 = LaserQtMainWindowSub01()
    myLaserQtSub02 = LaserQtMainWindowSub02()
    myLaserQtSub03 = LaserQtMainWindowSub03()
    myLaserQt.show()
    sys.exit(app.exec_())
