# -*- coding: utf-8 -*-e
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QSizePolicy

import os
FONT = FontProperties(fname=(os.getcwd() + "/LaserQt_Font/wqy-microhei.ttc"), size=10)

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.10
'''

class BaseCanvas(FigureCanvas):
    '''
    基类画布
    '''
    def __init__(self, figure):
        super(BaseCanvas, self).__init__(figure)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class StaticCanvasForPathInfo(BaseCanvas):
    '''
    静态路径信息画布，继承自基类画布
    '''
    def __init__(self, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim([0, 2])
        self.axes.set_xticks(np.arange(0, 22, 2)/10)
        self.axes.set_ylim([0, 1])
        self.axes.set_yticks(np.arange(0, 11)/10)
        self.axes.set_title("加工路径静态图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("X - 板长方向（m）", fontproperties=FONT, fontsize=9)
        self.axes.set_ylabel("Y - 板宽方向（m）", fontproperties=FONT, fontsize=9)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForPathInfo, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class DynamicCanvasForPathInfo(BaseCanvas):
    '''
    动态路径信息画布，继承自基类画布
    '''
    def __init__(self, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim([0, 2])
        self.axes.set_xticks(np.arange(0, 22, 2)/10)
        self.axes.set_ylim([0, 1])
        self.axes.set_yticks(np.arange(0, 11)/10)
        self.axes.set_title("加工路径动态图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("X - 板长方向（m）", fontproperties=FONT, fontsize=9)
        self.axes.set_ylabel("Y - 板宽方向（m）", fontproperties=FONT, fontsize=9)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(DynamicCanvasForPathInfo, self).__init__(figure=fig)
    
    def compute_initial_figure(self):
        pass

    def update_figure(self):
        pass


class Static3DCanvasForPointCloud(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=6, height=4, dpi=100):
        fig = plt.figure()
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = Axes3D(fig)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.set_zticks([])
        self.axes.set_xlabel("加工板水平方向", fontproperties=FONT, fontsize=9)
        self.axes.set_ylabel("加工板垂直方向", fontproperties=FONT, fontsize=9)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(Static3DCanvasForPointCloud, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class StaticCanvasForErrorCurve01(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=2, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工板水平方向1/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForErrorCurve01, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class StaticCanvasForErrorCurve02(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=2, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工板水平方向1/2处误差曲线图", fontproperties=FONT, fontsize=14)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForErrorCurve02, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class StaticCanvasForErrorCurve03(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=2, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工板水平方向2/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForErrorCurve03, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class StaticCanvasForErrorCurve04(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=2, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工板垂直方向1/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForErrorCurve04, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class StaticCanvasForErrorCurve05(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=2, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工板垂直方向2/3处误差曲线图", fontproperties=FONT, fontsize=14)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForErrorCurve05, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass


class StaticCanvasForErrorCurve06(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=2, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工板任意两点间误差曲线图", fontproperties=FONT, fontsize=14)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForErrorCurve06, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass