#!bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget

from LaserQt_Gui.LaserQt_Gui_Button import BrowseButton, NextButton, QuitButton, ConfirmButton

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.04
'''

class LaserQtMainWindow(QWidget):
    def __init__(self):
        super(LaserQtMainWindow, self).__init__()
        self.setStyleSheet('''
        QWidget{
            background-color: white;}
        ''')
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("复杂曲率板加工系统-开发者V1.0版")
        self.get_current_screen_size()
        self.resize(self.width, self.height)

        self.directoryLineEdit = QLineEdit()
        browseButton = BrowseButton()
        browseButton.clicked.connect(self.browse_directory)
        topLayout = QHBoxLayout()
        topLayout.addStretch()
        topLayout.addWidget(self.directoryLineEdit)
        topLayout.addWidget(browseButton)

        nextButton = NextButton()
        quitButton = QuitButton()
        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(0, 0, 20, 20)
        bottomLayout.addStretch()
        bottomLayout.addWidget(nextButton)
        bottomLayout.setSpacing(60)
        bottomLayout.addWidget(quitButton)

        widgetLayout = QGridLayout()
        widgetLayout.setContentsMargins(20, 20, 20, 20)
        widgetLayout.setSpacing(10)
        widgetLayout.addLayout(topLayout, 0, 0)
        widgetLayout.addLayout(bottomLayout, 1, 0)

        self.setLayout(widgetLayout)  

    def get_current_screen_size(self):
        self.width = 1366/1.1
        self.height = 768/1.1

    def browse_directory(self):
        mainDirectory = self.check_os()
        fileName, filetype= QFileDialog.getOpenFileName(self, "选取文件", mainDirectory, "All Files (*);;Text Files (*.txt)")
        self.directoryLineEdit.setText(fileName)

    def check_os(self):
        import platform
        if platform.system() == "Windows":
            return "C:/"

        elif platform.system() == "Linux":
            import getpass
            user = getpass.getuser()
            return "/home/" + user + "/"


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myLaserQt = LaserQtMainWindow()
    myLaserQt.show()
    sys.exit(app.exec_())
