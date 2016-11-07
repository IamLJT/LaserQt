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
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("加工路径图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("X - 板长方向", fontproperties=FONT)
        self.axes.set_ylabel("Y - 板宽方向", fontproperties=FONT)
        self.axes.grid(True, which="both")
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        super(BaseCanvas, self).__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        def compute_initial_figure(self):
            pass


class StaticCanvas(BaseCanvas):
    '''
    静态画布，继承自基类画布
    '''
    def compute_initial_figure(self):
        pass

class DynamicCanvas(BaseCanvas):
    '''
    动态画布，继承自基类画布
    '''
    def __init__(self, *args, **kwargs):
        super(DynamicCanvas, self).__init__(self, *args, **kwargs)
        pass

    def compute_initial_figure(self):
        pass

    def update_figure(self):
        pass
