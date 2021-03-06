# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created: Tue Dec 23 18:55:00 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Person = QtGui.QAction(MainWindow)
        self.actionNew_Person.setObjectName("actionNew_Person")
        self.actionNew_Relationship = QtGui.QAction(MainWindow)
        self.actionNew_Relationship.setObjectName("actionNew_Relationship")
        self.actionEdit_Person = QtGui.QAction(MainWindow)
        self.actionEdit_Person.setObjectName("actionEdit_Person")
        self.actionEdit_Relationship = QtGui.QAction(MainWindow)
        self.actionEdit_Relationship.setObjectName("actionEdit_Relationship")
        self.actionSave_Tree = QtGui.QAction(MainWindow)
        self.actionSave_Tree.setObjectName("actionSave_Tree")
        self.actionLoad_Tree = QtGui.QAction(MainWindow)
        self.actionLoad_Tree.setObjectName("actionLoad_Tree")
        self.actionNew_Tree = QtGui.QAction(MainWindow)
        self.actionNew_Tree.setObjectName("actionNew_Tree")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionDescendants = QtGui.QAction(MainWindow)
        self.actionDescendants.setObjectName("actionDescendants")
        self.actionHourglass = QtGui.QAction(MainWindow)
        self.actionHourglass.setObjectName("actionHourglass")
        self.actionPython = QtGui.QAction(MainWindow)
        self.actionPython.setObjectName("actionPython")
        self.actionPyside = QtGui.QAction(MainWindow)
        self.actionPyside.setObjectName("actionPyside")
        self.actionFamily_Tree = QtGui.QAction(MainWindow)
        self.actionFamily_Tree.setObjectName("actionFamily_Tree")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "My Family Tree", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Person.setText(QtGui.QApplication.translate("MainWindow", "New Person", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Relationship.setText(QtGui.QApplication.translate("MainWindow", "New Relationship", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Person.setText(QtGui.QApplication.translate("MainWindow", "Edit Person", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Relationship.setText(QtGui.QApplication.translate("MainWindow", "Edit Relationship", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Tree.setText(QtGui.QApplication.translate("MainWindow", "Save Tree", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Tree.setText(QtGui.QApplication.translate("MainWindow", "Load Tree", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Tree.setText(QtGui.QApplication.translate("MainWindow", "New Tree", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDescendants.setText(QtGui.QApplication.translate("MainWindow", "Descendants", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHourglass.setText(QtGui.QApplication.translate("MainWindow", "Hourglass", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPython.setText(QtGui.QApplication.translate("MainWindow", "Python", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPyside.setText(QtGui.QApplication.translate("MainWindow", "Pyside", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFamily_Tree.setText(QtGui.QApplication.translate("MainWindow", "Family Tree", None, QtGui.QApplication.UnicodeUTF8))

