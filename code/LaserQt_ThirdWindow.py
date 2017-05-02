# -*- coding: utf-8 -*-
# ********************系统自带相关模块导入********************
import ctypes  # 用于调用C++动态链接库
import os

import numpy as np
import pandas as pd
# ********************PyQt5相关模块导入********************
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
# ********************用户自定义相关模块导入********************
from LaserQt_AuxiliaryFunction import check_os, return_os, get_current_screen_size, get_current_screen_time
from LaserQt_Gui.LaserQt_Gui_Button import *
from LaserQt_Gui.LaserQt_Gui_Canvas import *
from LaserQt_Gui.LaserQt_Gui_Dialog import *

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.12
'''

class LaserQtThirdWindow(QWidget):
    '''
        系统第三个窗口页面类
    '''
    def __init__(self):
        super(LaserQtThirdWindow, self).__init__()
        self.targetDataFileName = ""
        self.scanningDataFileName = ""
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统")
        self.setWindowIcon(QIcon('LaserQt_Ui/logo_32px.png'))
        self.width, self.height = get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.widgetLayout)

    def set_widgets(self):
        targetDataLable = QLabel("目标数据")
        scanningDataLable = QLabel("扫描数据")
        self.targetDataDirectoryLineEdit = QLineEdit()
        self.scanningDataDirectoryLineEdit = QLineEdit()
        targetDataBrowseButton = BrowseButton()
        targetDataBrowseButton.clicked.connect(self.browse_target_data_directory)
        scanningDataBrowseButton = BrowseButton()
        scanningDataBrowseButton.clicked.connect(self.browse_scanning_data_directory)
        
        self.canvas = Static3DCanvasForPointCloud()
        canvasRegionLable = QLabel("点云拟合三维可视化")
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

        # 右半部分顶部布局
        rightTopLayout = QGridLayout()
        rightTopLayout.addWidget(targetDataLable, 0, 0)
        rightTopLayout.addWidget(scanningDataLable, 1, 0)
        rightTopLayout.addWidget(self.targetDataDirectoryLineEdit, 0, 1)
        rightTopLayout.addWidget(self.scanningDataDirectoryLineEdit, 1, 1)
        rightTopLayout.addWidget(targetDataBrowseButton, 0, 2)
        rightTopLayout.addWidget(scanningDataBrowseButton, 1, 2)

        logRegionLable = QLabel("后台执行过程展示区域")
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setEnabled(False)
        self.logTextEdit.setFontPointSize(12)
        self.executeProgressBar = QProgressBar()
        # 右半部分中部布局
        rightMiddleLayout = QVBoxLayout()
        rightMiddleLayout.addWidget(logRegionLable)
        rightMiddleLayout.addWidget(self.logTextEdit)
        rightMiddleLayout.addWidget(self.executeProgressBar)

        self.elevationSlider = QSlider()
        self.elevationSlider.setOrientation(Qt.Horizontal)
        self.elevationSlider.setMinimum(0)
        self.elevationSlider.setMaximum(180)
        self.elevationSlider.setSingleStep(5)
        self.elevationSlider.valueChanged.connect(self.elevation_slider_value_changed)
        self.elevationSpinBox = QSpinBox()
        self.elevationSpinBox.setMinimum(0)
        self.elevationSpinBox.setMaximum(180)
        self.elevationSpinBox.setSingleStep(5)
        self.elevationSpinBox.valueChanged.connect(self.elevation_spinbox_value_changed)
        self.azimuthSlider = QSlider()
        self.azimuthSlider.setOrientation(Qt.Horizontal)
        self.azimuthSlider.setMinimum(-180)
        self.azimuthSlider.setMaximum(180)
        self.azimuthSlider.setSingleStep(5)
        self.azimuthSlider.valueChanged.connect(self.azimuth_slider_value_changed)
        self.azimuthSpinBox = QSpinBox()
        self.azimuthSpinBox.setMinimum(-180)
        self.azimuthSpinBox.setMaximum(180)
        self.azimuthSpinBox.setSingleStep(5)
        self.azimuthSpinBox.valueChanged.connect(self.azimuth_spinbox_value_changed)
        sliderLayout = QGridLayout()
        sliderLayout.addWidget(self.elevationSlider, 0, 0, 1, 8)
        sliderLayout.addWidget(QLabel("俯仰角"), 0, 8, 1, 1)
        sliderLayout.addWidget(self.elevationSpinBox, 0, 9, 1, 1)
        sliderLayout.addWidget(self.azimuthSlider, 1, 0, 1, 8)
        sliderLayout.addWidget(QLabel("方位角"), 1, 8, 1, 1)
        sliderLayout.addWidget(self.azimuthSpinBox, 1, 9, 1, 1)

        pointCloudDataScanButton = PointCloudDataScanButton()
        pointCloudDataScanButton.clicked.connect(self.point_cloud_data_scan)
        self.pointCloudDataDenoisingButton = PointCloudDataDenoisingButton()
        self.pointCloudDataDenoisingButton.clicked.connect(self.point_cloud_data_denoising)
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
        rightLayout.addLayout(rightTopLayout)
        rightLayout.addLayout(rightMiddleLayout)
        rightLayout.addLayout(sliderLayout)
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

    # 
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

    # 点云数据扫描
    def point_cloud_data_scan(self):
        # if self.scanningDataFileName == "":
        #     messageDialog = MessageDialog()
        #     messageDialog.warning(self, "消息提示对话框", "请先加载扫描数据!", messageDialog.Yes, messageDialog.Yes)
        #     return

        self.logTextEdit.setText("")  # 清空日志窗口
        # self.put_info_into_log("开始点云数据扫描...", 0)

        # 点云扫描过程
        messageDialog = MessageDialog()
        import yaml
        import subprocess
        with open("faro_config.yaml", 'r') as fd:
            yaml_file = yaml.load(fd)
            faro_sdk = yaml_file["FAROSDKDemoApp"]["dir"]
            faro_open = yaml_file["FAROOpenDemoApp"]["dir"]
        reply = messageDialog.information(self, "消息提示对话框", "FAROSDKDemoApp可执行程序路径：\n{}".format(faro_sdk), 
            messageDialog.Yes | messageDialog.No, messageDialog.Yes)
        if reply == messageDialog.Yes:
            subprocess.Popen(faro_sdk)
            reply = messageDialog.information(self, "消息提示对话框", "FAROOpenDemoApp可执行程序路径：\n{}\n在执行FAROOpenDemoApp前，请确保已执行FAROSDKDemoApp".format(faro_open),
                messageDialog.Yes | messageDialog.No, messageDialog.Yes)
            if reply == messageDialog.Yes:
                subprocess.Popen(faro_open)
        
        # self.put_info_into_log("点云数据扫描完毕...", 100)

        self.hasDoDenoising = True
        self.pointCloudDataDenoisingButton.setEnabled(True)

    # 点云数据去噪
    def point_cloud_data_denoising(self):
        self.logTextEdit.setText("")
        self.put_info_into_log("开始点云数据去噪...", 0)

        # 调用点云去噪算法
        if "Windows" == return_os():
             self.dll = ctypes.CDLL("LaserQt_Algorithm/C++_Windows/PointCloudAlgorithm/Debug/PointCloudAlgorithm.dll")  # 创建动态链接库对象
        elif "Linux" == return_os():
             self.dll = ctypes.CDLL("LaserQt_Algorithm/C++_Linux/PointCloudAlgorithm.so")  # 创建动态链接库对象

        inpath = ctypes.create_string_buffer(bytes(self.scanningDataFileName.encode("gbk")))  # 创建C/C++可调用的字符串对象

        removedNoise = self.dll.PointCloudKThreshlod(inpath)  # 获取噪声点数并初步去噪
        residualNoise = 0

        # 这里应提示是否进行平滑处理
        # self.dll.PointCloudDenoise();  # 调用C++函数 void PointCloudDenoise()

        self.put_info_into_log("点云数据去噪完毕...", 100)

        messageDialog = MessageDialog()
        reply = messageDialog.information(self, "消息提示对话框", "本次去噪共去除噪声点{}个，剩余噪声点{}个！是否需要保存数据？".format(removedNoise, residualNoise), messageDialog.Yes | messageDialog.No, messageDialog.Yes)
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

    # 点云数据拟合
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
            inpath = ctypes.create_string_buffer(bytes(self.scanningDataFileName.encode("gbk")))  # 创建C/C++可调用的字符串对象，扫描文件路径
            outpath = ctypes.create_string_buffer(bytes(self.targetDataFileName.encode("gbk")))  # 目标文件路径
            isFilter = 1  # 需要进行判断，是否需要平滑？
            self.dll = ctypes.CDLL("LaserQt_Algorithm/C++_Windows/PointCloudAlgorithm/Debug/PointCloudAlgorithm.dll")
            self.dll.PointCloudFitting(inpath, isFilter, outpath)  # 调用C++函数 void PointCloudFitting(const char* path, bool isFilter, const char* targetData)
            # fittingDataFileName = self.dll.PointCloudFitting(inpath, isFilter, outpath)

            self.put_info_into_log("点云数据拟合完成...", 100)

            fittingDataFileName = "LaserQt_Material/FittingData.txt"  # TODO

        self.canvas.axes.plot([0], [0])
        self.canvas.axes.hold(True)
        self.canvas.axes.set_xticks([])
        self.canvas.axes.set_yticks([])
        self.canvas.axes.set_zticks([])
        self.canvas.axes.set_xlabel("加工板X方向", fontproperties=FONT, fontsize=9)
        self.canvas.axes.set_ylabel("加工板Y方向", fontproperties=FONT, fontsize=9)
        self.canvas.axes.set_zlabel("加工板Z方向", fontproperties=FONT, fontsize=9)
        self.canvas.axes.grid(True, which="both") 

        dataframe = pd.read_csv(self.targetDataFileName, header=None)
        dataframe.dropna()
        self.matrix1 = dataframe.as_matrix()
        self.canvas.axes.scatter(self.matrix1[::10, 0], self.matrix1[::10, 1], self.matrix1[::10, 2], c='red')
        dataframe = pd.read_csv(fittingDataFileName, header=None)
        dataframe.dropna()
        self.matrix2 = dataframe.as_matrix()
        self.canvas.axes.scatter(self.matrix2[:, 0], self.matrix2[:, 1], self.matrix2[:, 2], c='black')

        self.canvas.axes.set_xlim([np.min(self.matrix1[:, 0]), np.max(self.matrix1[:, 0])])
        self.canvas.axes.set_ylim([np.min(self.matrix1[:, 1]), np.max(self.matrix1[:, 1])])
        self.canvas.axes.set_zlim([np.min(self.matrix1[:, 2]), np.max(self.matrix1[:, 2])])

        # elevation 0 - 180  
        # azimuth   -180 - 180
        self.canvas.draw()
        
        self.canvas.axes.hold(False)
        messageDialog = MessageDialog()
        messageDialog.question(self, "消息提示对话框", "绘图完毕！", messageDialog.Yes, messageDialog.Yes)

        self.hasDoDenoising = False

    def put_info_into_log(self, info, progressValue):
        self.logTextEdit.append("[ {} ] : {}".format(get_current_screen_time(), info))
        self.executeProgressBar.setValue(progressValue)
        qApp.processEvents()  # 强制刷新界面

    def elevation_slider_value_changed(self):
        pass
        # self.elevationSpinBox.setValue(self.elevationSlider.value())
        # self.canvas.axes.view_init(self.elevationSlider.value(), self.azimuthSlider.value())
        # self.canvas.draw()

    def elevation_spinbox_value_changed(self):
        self.elevationSlider.setValue(self.elevationSpinBox.value())
        self.canvas.axes.view_init(self.elevationSpinBox.value(), self.azimuthSpinBox.value())
        self.canvas.draw()

    def azimuth_slider_value_changed(self):
        pass
        # self.azimuthSpinBox.setValue(self.azimuthSlider.value())
        # self.canvas.axes.view_init(self.elevationSlider.value(), self.azimuthSlider.value())
        # self.canvas.draw()

    def azimuth_spinbox_value_changed(self):
        self.azimuthSlider.setValue(self.azimuthSpinBox.value())
        self.canvas.axes.view_init(self.elevationSpinBox.value(), self.azimuthSpinBox.value())
        self.canvas.draw()
