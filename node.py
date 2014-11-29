from PySide import QtCore, QtGui
import sys
import datetime

months = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', 
          '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', 
          '11':'Nov', '12':'Dec'}

class Actor(QtGui.QGraphicsWidget):
    nick_name = ''
    real_name = ''
    gender = ''
    bday = ''
    age = ''
    marital = ''
    children = ''
    death = ''
    important = False
    def __init__(self, nick_name, real_name, gender, bday, age, marital, children, death, important, parent=None):
        super(Actor, self).__init__(parent)
        self.nick_name = nick_name
        self.real_name = real_name
        self.gender = gender
        self.bday = bday
        self.age = age
        self.marital = marital
        self.children = children
        self.death = death
        self.important = important
        
    
    def headerRect(self):
        return QtCore.QRectF(-55,-60,110,35)
    
    def boundingRect(self):
        return QtCore.QRectF(-60, -60, 120, 120)    
        
    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())

        return path
    
    def paint(self, painter, option, widget):
        r = self.boundingRect()
        h = self.headerRect()
        
        painter.setBrush(QtGui.QColor.fromHsv(255,0,255,160))
        painter.drawEllipse(r)        

        if self.gender == 'M':
            painter.setBrush(QtGui.QColor.fromHsv(240,255,255,255))
        elif self.gender == 'F':
            painter.setBrush(QtGui.QColor.fromHsv(0,255,255,255))
        painter.drawRoundedRect(h,5,5)
        
        text = self.nick_name
        painter.setPen(QtCore.Qt.white)
        painter.drawText(h,QtCore.Qt.AlignCenter, text)
        
        
        text = '\n'.join((self.real_name, str(self.age) + ' - ' + self.marital, 
                          self.bday, 'Children: ' + str(self.children)))
        painter.setPen(QtCore.Qt.black)
        painter.drawText(r,QtCore.Qt.AlignCenter, text)        
        
        
    
class View(QtGui.QGraphicsView):
    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene(-350,-350,700,700)
    
    actor = Actor('Akber','Akber Ali','M','1991-Jan-28', 23,'Single',0,'2051-Jan-28',True)
    actor.setPos(0,0)
    
    scene.addItem(actor)
    
    view = View(scene)
    view.setWindowTitle("Animated Tiles")
    view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
    view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
    view.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
    view.show()
    
    sys.exit(app.exec_())