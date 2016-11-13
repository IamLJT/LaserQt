# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_AuxiliaryFunction import check_os, get_current_screen_size
from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import *
from LaserQt_Gui.LaserQt_Gui_Dialog import *

import queue
import threading
import time

import xlrd

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class LaserQtSecondWindow(QWidget):
    def __init__(self):
        super(LaserQtSecondWindow, self).__init__()
        self.fileName = ""
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
        self.canvas = DynamicCanvasForPathInfo() ## TODO
        canvasRegionLable = QLabel("数据可视化区域")
        qFont = QFont()
        qFont.setPointSize(12)
        canvasRegionLable.setFont(qFont)
        # 左半部分中部布局
        leftMiddleLayout = QVBoxLayout()
        leftMiddleLayout.setSpacing(10)
        leftMiddleLayout.addWidget(canvasRegionLable)
        leftMiddleLayout.addWidget(self.canvas)

        self.prevButton = PreviousButton()
        self.nextButton = NextButton()
        quitButton = QuitButton()
        # 左半部分底部布局
        leftBottomLayout = QHBoxLayout()
        leftBottomLayout.addStretch()
        leftBottomLayout.setSpacing(60)
        leftBottomLayout.addWidget(self.prevButton)
        leftBottomLayout.addWidget(self.nextButton)
        leftBottomLayout.addWidget(quitButton)

        # 左半部分布局
        leftLayout = QVBoxLayout()
        leftLayout.setSpacing(23)
        leftLayout.addLayout(leftMiddleLayout)
        leftLayout.addLayout(leftBottomLayout)

        tableRegionLable = QLabel("数据实时显示区域")
        tableRegionLable.setFont(qFont)
        dataShowLayout = QGridLayout()

        dataShow01Lable = QLabel("加载文件")
        dataShow01Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow01Lable, 0, 0)
        self.dataShow01Edit = QLineEdit()
        dataShowLayout.addWidget(self.dataShow01Edit, 0, 1)
        browseButton = BrowseButton()
        browseButton.clicked.connect(self.browse_directory)
        dataShowLayout.addWidget(browseButton, 0, 2)

        dataShow02Lable = QLabel("路径编号")
        dataShow02Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow02Lable, 1, 0)
        self.dataShow02Edit = QLineEdit()
        self.dataShow02Edit.setEnabled(False)
        dataShowLayout.addWidget(self.dataShow02Edit, 1, 1)

        dataShow03Lable = QLabel("起点坐标")
        dataShow03Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow03Lable, 2, 0)
        self.dataShow03Edit = QLineEdit()
        self.dataShow03Edit.setEnabled(False)
        dataShowLayout.addWidget(self.dataShow03Edit, 2, 1)

        dataShow04Lable = QLabel("终点坐标")
        dataShow04Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow04Lable, 3, 0)
        self.dataShow04Edit = QLineEdit()
        self.dataShow04Edit.setEnabled(False)
        dataShowLayout.addWidget(self.dataShow04Edit, 3, 1)

        dataShow05Lable = QLabel("下压量")
        dataShow05Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow05Lable, 4, 0)
        self.dataShow05Edit = QLineEdit()
        self.dataShow05Edit.setEnabled(False)
        dataShowLayout.addWidget(self.dataShow05Edit, 4, 1)

        dataShow06Lable = QLabel("热参数")
        dataShow06Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow06Lable, 5, 0)
        self.dataShow06Edit = QLineEdit()
        self.dataShow06Edit.setEnabled(False)
        dataShowLayout.addWidget(self.dataShow06Edit, 5, 1)

        dataShow07Lable = QLabel("加工时间")
        dataShow07Lable.setFont(qFont)
        dataShowLayout.addWidget(dataShow07Lable, 6, 0)
        self.dataShow07Edit = QLineEdit()
        self.dataShow07Edit.setEnabled(False)
        dataShowLayout.addWidget(self.dataShow07Edit, 6, 1)
        # 右半部分中部布局
        rightMiddleLayout = QVBoxLayout()
        rightMiddleLayout.setSpacing(52)
        rightMiddleLayout.addWidget(tableRegionLable)
        rightMiddleLayout.addLayout(dataShowLayout)
        
        startProcessingButton = StartProcessingButton()
        startProcessingButton.clicked.connect(self.start_processing)
        self.timer = QTimer() # 初始化定时器对象
        self.timer.timeout.connect(self.time_count)
        self.mplThread = threading.Thread(target=self.socket_communication) ## 初始化socket通信子线程
        self.mplThread.setDaemon(True)
        self.stopProcessingButton = StopProcessingButton()
        self.stopProcessingButton.setEnabled(False)
        self.stopProcessingButton.clicked.connect(self.stop_processing)
        self.continueProcessingButton = ContinueProcessingButton()
        self.continueProcessingButton.setEnabled(False)
        self.continueProcessingButton.clicked.connect(self.continue_processing)
        # 右半部分底部布局
        rightBottomLayout = QHBoxLayout()
        rightBottomLayout.addStretch()
        rightBottomLayout.setSpacing(62)
        rightBottomLayout.addWidget(startProcessingButton)
        rightBottomLayout.addWidget(self.stopProcessingButton)
        rightBottomLayout.addWidget(self.continueProcessingButton)

        # 右半部分布局
        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(75)
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

    def browse_directory(self):
        mainDirectory = check_os()
        currentFileDialog = OpenFileDialog()
        fileName, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Excel Files (*.xlsx)")
        if fileName != "":
            self.fileName = fileName
            self.dataShow01Edit.setText(self.fileName)

    def init_task_queue(self):
        self.myTaskQueue = queue.Queue(maxsize=100) # 任务队列 -- 生产者-消费者模式
        if self.fileName == "":
            return -1
        excelReadOnly = xlrd.open_workbook(self.fileName)
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
        ret = self.init_task_queue()
        if ret == -1:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "请先加载文件!", messageDialog.Yes, messageDialog.Yes)
            return
        self.isStop = False
        self.stopProcessingButton.setEnabled(True)

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
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示对话框", "所有路径加工完毕！", messageDialog.Yes, messageDialog.Yes)
        else:
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示对话框", "您已停止加工！", messageDialog.Yes, messageDialog.Yes)

    def stop_processing(self):
        self.isStop = True
        self.continueProcessingButton.setEnabled(True)

    def continue_processing(self):
        messageDialog = MessageDialog()
        messageDialog.information(self, "消息提示对话框", "您将开始加工！", messageDialog.Yes, messageDialog.Yes)

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
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示对话框", "所有路径加工完毕！", messageDialog.Yes, messageDialog.Yes)
        else:
            messageDialog = MessageDialog()
            messageDialog.information(self, "消息提示对话框", "您已停止加工！", messageDialog.Yes, messageDialog.Yes)

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