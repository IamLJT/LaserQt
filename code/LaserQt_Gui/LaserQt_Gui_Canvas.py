# -*- coding: utf-8 -*-
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.04
'''

class BaseCanvas(FigureCanvas):
    '''
    基类画布
    '''
    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        super(BaseCanvas, self).__init__(fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
