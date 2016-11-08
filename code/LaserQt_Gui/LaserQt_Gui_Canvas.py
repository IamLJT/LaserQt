# -*- coding: utf-8 -*-e
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from PyQt5.QtWidgets import QSizePolicy

import os
FONT = FontProperties(fname=(os.getcwd() + "/LaserQt_Font/wqy-microhei.ttc"), size=10)

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.07
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
        self.axes.set_title("加工路径静态图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("X - 板长方向", fontproperties=FONT, fontsize=9)
        self.axes.set_ylabel("Y - 板宽方向", fontproperties=FONT, fontsize=9)
        self.axes.grid(True, which="both")
        self.axes.arrow(0.05, 0.05, 0, 0.1)
        self.axes.arrow(0.05, 0.05, 0.1, 0)
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
        self.axes.set_title("加工路径动态图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("X - 板长方向", fontproperties=FONT, fontsize=9)
        self.axes.set_ylabel("Y - 板宽方向", fontproperties=FONT, fontsize=9)
        self.axes.grid(True, which="both")
        self.axes.arrow(0.05, 0.05, 0, 0.1)
        self.axes.arrow(0.05, 0.05, 0.1, 0)
        # We want the axes cleared every time plot() is called
        self.axes.hold(True)
        super(DynamicCanvasForPathInfo, self).__init__(figure=fig)
    
    def compute_initial_figure(self):
        pass

    def update_figure(self):
        pass

class StaticCanvasForPointCloud(BaseCanvas):
    '''
    静态点云数据拟合画布，继承自基类画布
    '''
    def __init__(self, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("点云拟合图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("X", fontproperties=FONT, fontsize=9)
        self.axes.set_ylabel("Y", fontproperties=FONT, fontsize=9)
        self.axes.grid(True, which="both")
        self.axes.arrow(0.05, 0.05, 0, 0.1)
        self.axes.arrow(0.05, 0.05, 0.1, 0)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        super(StaticCanvasForPointCloud, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass
