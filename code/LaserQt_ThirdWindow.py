# #-*- coding: utf-8 -*-
# -*- coding: gb18030 -*- 
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_AuxiliaryFunction import check_os, return_os, get_current_screen_size, get_current_screen_time
from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import *
from LaserQt_Gui.LaserQt_Gui_Dialog import *

import ctypes
import os

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class LaserQtThirdWindow(QWidget):
    def __init__(self):
        super(LaserQtThirdWindow, self).__init__()
        self.targetDataFileName = ""
        self.scanningDataFileName = ""
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
        targetDataLable = QLabel("目标数据")
        qFont = QFont()
        qFont.setPointSize(12)
        targetDataLable.setFont(qFont)
        scanningDataLable = QLabel("扫描数据")
        scanningDataLable.setFont(qFont)
        self.targetDataDirectoryLineEdit = QLineEdit()
        # self.targetDataDirectoryLineEdit.setText("D:\PyQt\LaserQt\code\LaserQt_Material\目标数据.txt") ## TODO
        # self.targetDataFileName = "D:\PyQt\LaserQt\code\LaserQt_Material\目标数据.txt"
        self.scanningDataDirectoryLineEdit = QLineEdit()
        # self.scanningDataDirectoryLineEdit.setText("D:\PyQt\LaserQt\code\LaserQt_Material\测试数据.txt")
        # self.scanningDataFileName = "D:\PyQt\LaserQt\code\LaserQt_Material\测试数据.txt"
        targetDataBrowseButton = BrowseButton()
        targetDataBrowseButton.clicked.connect(self.browse_target_data_directory)
        scanningDataBrowseButton = BrowseButton()
        scanningDataBrowseButton.clicked.connect(self.browse_scanning_data_directory)
        # 左半部分顶部布局
        leftTopLayout = QGridLayout()
        leftTopLayout.addWidget(targetDataLable, 0, 0)
        leftTopLayout.addWidget(scanningDataLable, 1, 0)
        leftTopLayout.addWidget(self.targetDataDirectoryLineEdit, 0, 1)
        leftTopLayout.addWidget(self.scanningDataDirectoryLineEdit, 1, 1)
        leftTopLayout.addWidget(targetDataBrowseButton, 0, 2)
        leftTopLayout.addWidget(scanningDataBrowseButton, 1, 2)
        
        self.canvas = Static3DCanvasForPointCloud()
        canvasRegionLable = QLabel("点云拟合三维可视化")
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
        leftLayout.addLayout(leftTopLayout)
        leftLayout.addLayout(leftMiddleLayout)
        leftLayout.addLayout(leftBottomLayout)

        logRegionLable = QLabel("后台执行过程展示区域")
        logRegionLable.setFont(qFont)
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setEnabled(False)
        self.logTextEdit.setFontPointSize(12)
        self.executeProgressBar = QProgressBar()
        # 右半部分中部布局
        rightMiddleLayout = QVBoxLayout()
        rightMiddleLayout.addWidget(logRegionLable)
        rightMiddleLayout.addWidget(self.logTextEdit)
        rightMiddleLayout.addWidget(self.executeProgressBar)

        pointCloudDataScanButton = PointCloudDataScanButton()
        pointCloudDataScanButton.clicked.connect(self.point_cloud_data_scan)
        self.pointCloudDataDenoisingButton = PointCloudDataDenoisingButton()
        self.pointCloudDataDenoisingButton.clicked.connect(self.point_cloud_data_denoising )
        self.pointCloudDataDenoisingButton.setEnabled(False)
        pointCloudDataFittingButton = PointCloudDataFittingButton()
        pointCloudDataFittingButton.clicked.connect(self.point_cloud_data_fitting)
        # 右半部分底部布局
        rightBottomLayout = QHBoxLayout()
        rightBottomLayout.addStretch()
        rightBottomLayout.addWidget(pointCloudDataScanButton)
        rightBottomLayout.addWidget(self.pointCloudDataDenoisingButton)
        rightBottomLayout.addWidget(pointCloudDataFittingButton)

        # 右半部分布局
        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(23)
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

    def browse_target_data_directory(self): ## TODO
        mainDirectory = check_os()
        # 打开文件选择对话框
        currentFileDialog = OpenFileDialog()
        fileName, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Text Files (*.txt)")
        if fileName != "":
            self.targetDataFileName = fileName
            self.targetDataDirectoryLineEdit.setText(self.targetDataFileName)

    def browse_scanning_data_directory(self): ## TODO
        mainDirectory = check_os()
        # 打开文件选择对话框
        currentFileDialog = OpenFileDialog()
        filename, filetype= currentFileDialog.open_file(self, caption="选取文件", directory=mainDirectory, filter="Text Files (*.txt)")
        if filename != "":
            self.scanningDataFileName = filename
            self.scanningDataDirectoryLineEdit.setText(self.scanningDataFileName)
        self.hasDoDenoising = False

    def point_cloud_data_scan(self):
        if self.scanningDataFileName == "":
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "请先加载扫描数据!", messageDialog.Yes, messageDialog.Yes)
            return

        self.logTextEdit.setText("")  # 清空日志窗口
        self.put_info_into_log("开始点云数据扫描...", 0)

        # 点云扫描过程

        self.put_info_into_log("点云数据扫描完毕...", 100)

        self.hasDoDenoising = True
        self.pointCloudDataDenoisingButton.setEnabled(True)

    def point_cloud_data_denoising(self):
        self.logTextEdit.setText("")
        self.put_info_into_log("开始点云数据去噪...", 0)

        # 调用点云去噪算法
        if "Windows" == return_os():
           #  self.dll = ctypes.CDLL("LaserQt_Algorithm/C++/PointCloudAlgorithm.dll")  # 创建动态链接库对象
             self.dll = ctypes.LibraryLoader("LaserQt_Algorithm/DLL_Generate/Debug/PointCloudAlgorithm.dll")  # 创建动态链接库对象
           #  self.dll = ctypes.CDLL("LaserQt_Algorithm/C++/libPointCloudAlgorithm.a")  # 创建静态链接库对象
        elif "Linux" == return_os():
             self.dll = ctypes.CDLL("LaserQt_Algorithm/C++/PointCloudAlgorithm.so")  # 创建动态链接库对象
        # path = ctypes.create_string_buffer(bytes(self.scanningDataFileName.encode("utf-8")))  # 创建C/C++可调用的字符串对象
        #path = "C:/Users/Iam_luffy/Documents/GitHub/LaserQt/code/LaserQt_Material/测试数据.txt"
        print(self.dll)
        
        #noisenum = self.dll.PointCloudKThreshlod("C:\\Users\\Iam_luffy\\Documents\\GitHub\\LaserQt\\code\\LaserQt_Material\\测试数据.txt")  # 获取噪声点数并初步去噪
        #print(noisenum)
        self.dll.PointCloudDenoise()
       # self.dll.PointCloudDenoise(path)  # 调用那个C++函数 void PointCloudDenoise(const char* path)

        self.put_info_into_log("点云数据去噪完毕...", 100)

        messageDialog = MessageDialog()
        reply = messageDialog.information(self, "消息提示对话框", "本次去噪共去除噪声点XX个，剩余噪声点XX个！是否需要保存数据？", messageDialog.Yes | messageDialog.No, messageDialog.Yes)
        if reply == messageDialog.No:
            return

        # 打开文件保存对话框
        currentFileDialog = SaveFileDialog()
        filename, filetype = currentFileDialog.save_file(self, caption="保存文件", filter="Text Files (*.txt)")
        if filename == "":
            messageDialog.warning(self, "消息提示对话框", "您已取消保存!", messageDialog.Yes, messageDialog.Yes)
        else:
            with open(filename, 'w') as fd1:
                with open("LaserQt_Material/tempData.txt", 'r') as fd2:
                    for line in fd2:
                        fd1.write(line)

    def point_cloud_data_fitting(self):
        if self.targetDataFileName == "":
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "请先加载目标数据!", messageDialog.Yes, messageDialog.Yes)
            return
        elif self.scanningDataFileName == "":
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "请先加载扫描数据!", messageDialog.Yes, messageDialog.Yes)
            return

        if not self.hasDoDenoising:
            messageDialog = MessageDialog()
            reply = messageDialog.question(self, "消息提示对话框", "您未作点云去噪处理，需要预览初始拟合效果吗？", messageDialog.Yes | messageDialog.No, messageDialog.No)
            if reply == messageDialog.No:
                return
            fittingDataFileName = self.scanningDataFileName
        else:
            self.logTextEdit.setText("")
            self.put_info_into_log("开始点云数据拟合...", 0)

            # 调用点云拟合算法  
            # path = ctypes.create_string_buffer(bytes("LaserQt_Material/tempData.txt".encode("utf-8")))  # 创建C/C++可调用的字符串对象
            # self.dll.PointCloudFitting()  # 调用那个C++函数 void PointCloudFitting(const char* path, bool isFilter, const char* targetData)

            self.put_info_into_log("点云数据拟合完成...", 100)

            fittingDataFileName = "LaserQt_Material/输出数据.txt"

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

        X = []; Y = []; self.Z1 = []  # X， Y的取值介于1～100？
        X = [[_] * 100 for _ in range(1, 101)] 
        Y = [_ for _ in range(1, 101)] * 100
        with open(self.targetDataFileName, 'r') as fd:
            for line in fd:
                dataCell = line.strip().split(',')
                self.Z1.append(float(dataCell[2]))
        self.canvas.axes.scatter(X, Y, self.Z1, c='red')
        self.Z2 = []
        with open(fittingDataFileName, 'r') as fd:
            for line in fd:
                dataCell = line.strip().split(',')
                self.Z2.append(float(dataCell[2]))
        self.canvas.axes.scatter(X, Y, self.Z2, c='black')

        self.canvas.draw()
        
        self.canvas.axes.hold(False)
        messageDialog = MessageDialog()
        messageDialog.question(self, "消息提示对话框", "绘图完毕！", messageDialog.Yes, messageDialog.Yes)

        self.hasDoDenoising = False

    def put_info_into_log(self, info, progressValue):
        self.logTextEdit.append("[ {} ] : {}".format(get_current_screen_time(), info))
        self.executeProgressBar.setValue(progressValue)
        qApp.processEvents() # 强制刷新界面
