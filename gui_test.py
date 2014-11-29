from PySide.QtCore import *
from PySide.QtGui import *
import sys

import mainwindow

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.connect(self.actionExit, SIGNAL('clicked()'),self.exitApp)
        
    def exitApp(self):
        sys.exit(0)
        
app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()