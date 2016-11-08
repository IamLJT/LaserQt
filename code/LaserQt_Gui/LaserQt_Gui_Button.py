# -*- coding: utf-8 -*-
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

'''
QMessageBox.information 信息框
QMessageBox.question    问答框
QMessageBox.warning     警告框
QMessageBox.ctitical    危险框
QMessageBox.about       关于框
'''

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.07
'''

class BaseButton(QPushButton):
    '''
    基类按钮
    '''
    def __init__(self, name=""):
        super(BaseButton, self).__init__(name)


class BrowseButton(BaseButton):
    '''
    浏览按钮，继承自基类按钮
    '''
    def __init__(self):
        super(BrowseButton, self).__init__(name="浏览")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class PreviousButton(BaseButton):
    '''
    上一步按钮，继承自基类按钮
    '''
    def __init__(self):
        super(PreviousButton, self).__init__(name="上一步")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class NextButton(BaseButton):
    '''
    下一步按钮，继承自基类按钮
    '''
    def __init__(self):
        super(NextButton, self).__init__(name="下一步")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class ConfirmButton(BaseButton):
    '''
    确认按钮，继承自基类按钮
    '''
    def __init__(self):
        super(ConfirmButton, self).__init__(name="确认")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class CancelButton(BaseButton):
    '''
    取消按钮，继承自基类按钮
    '''
    def __init__(self):
        super(CancelButton, self).__init__(name="取消")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class QuitButton(BaseButton):
    '''
    退出按钮，继承自基类按钮
    '''
    def __init__(self):
        super(QuitButton, self).__init__(name="退出")
        self.function_init()
    
    # 功能绑定 - 弹出消息提示对话框
    def function_init(self):
        self.clicked.connect(self.pop_up_hint_dialog)

    # 弹出消息提示对话框
    def pop_up_hint_dialog(self):
        reply = QMessageBox.question(self, "消息提示对话框", "您要退出系统吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCoreApplication.instance().quit()
        else:
            pass


class EditButton(BaseButton):
    '''
    编辑按钮，继承自基类按钮
    '''
    def __init__(self):
        super(EditButton, self).__init__(name="开启编辑")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class UpdateButton(BaseButton):
    '''
    更新按钮，继承自基类按钮
    '''
    def __init__(self):
        super(UpdateButton, self).__init__(name="更新路径")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class StartProcessingButton(BaseButton):
    '''
    开始加工按钮，继承自基类按钮
    '''
    def __init__(self):
        super(StartProcessingButton, self).__init__(name="开始加工")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class StopProcessingButton(BaseButton):
    '''
    停止加工按钮，继承自基类按钮
    '''
    def __init__(self):
        super(StopProcessingButton, self).__init__(name="停止加工")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class ContinueProcessingButton(BaseButton):
    '''
    继续加工按钮，继承自基类按钮
    '''
    def __init__(self):
        super(ContinueProcessingButton, self).__init__(name="继续加工")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class PointCloudDataScanButton(BaseButton):
    '''
    点云数据扫描按钮，继承自基类按钮
    '''
    def __init__(self):
        super(PointCloudDataScanButton, self).__init__(name="点云扫描")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class PointCloudDataDenoisingButton(BaseButton):
    '''
    点云数据去噪按钮，继承自基类按钮
    '''
    def __init__(self):
        super(PointCloudDataDenoisingButton, self).__init__(name="点云去噪")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass


class PointCloudDataFittingButton(BaseButton):
    '''
    点云数据拟合按钮，继承自基类按钮
    '''
    def __init__(self):
        super(PointCloudDataFittingButton, self).__init__(name="点云拟合")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass
