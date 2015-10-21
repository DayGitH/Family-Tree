from PySide.QtCore import *
from PySide.QtGui import *
import sys
import node
import ascend
import descend
import csv_handle
import mainwindow

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.connect(self.actionExit, SIGNAL('clicked()'),self.exitApp)

    def exitApp(self):
        sys.exit(0)

class View(QGraphicsView):
    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

def main():
    app = QApplication(sys.argv)

    form = MainWindow()

    scene = QGraphicsScene(-9600,-5400,19200,10800)

    people = csv_handle.load('Family tree test.csv')

    a_list = ascend.create_scene(people,'009')
    for i in a_list:
        scene.addItem(a_list[i])

    b_list = descend.create_scene(people,'009')
    for i in b_list:
        scene.addItem(b_list[i])
    form.graphicsView.setScene(scene)

    form.showMaximized()

    form.show()
    app.exec_()

if __name__ == '__main__':
    main()