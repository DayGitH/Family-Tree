from PySide.QtCore import *
from PySide.QtGui import *
import sys
import gui_test
import subprocess
import time

import showGui


class MainDialog(QDialog, showGui.Ui_mainDialog):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.showButton.setText("Process")
        self.connect(self.showButton, SIGNAL("clicked()"), self.processData)

        self.workerThread = WorkerThread()
        self.connect(self.workerThread, SIGNAL("threadDone(QString, QString)"), self.threadDone, Qt.DirectConnection)

    def processData(self):
        self.workerThread.start()
        QMessageBox.information(self, "Done!", "Done.")

    def threadDone(self, text, text2):
        self.nameEdit.setText("Worker thread finished processing.")
        print(text)
        print(text2)




class WorkerThread(QThread):

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        subprocess.Popen('Python gui_test.py',shell=False)



app = QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()