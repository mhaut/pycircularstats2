from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QObject,QEvent,pyqtSignal, Qt



class mouseEvent(QObject):
    mouseDoubleClicked=pyqtSignal(QMouseEvent)
    mousePressed=pyqtSignal(QMouseEvent)
    mouseReleased=pyqtSignal(QMouseEvent)
    mousePositionChange=pyqtSignal(QMouseEvent)
    def __init__(self,parent=None):
        QObject.__init__(self,parent=parent)

    def eventFilter(self, obj=QObject, event=QEvent):
        res=True
        if   event.type() == QEvent.MouseButtonDblClick:
            self.mouseDoubleClicked.emit(QMouseEvent(event))
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.mousePressed.emit(QMouseEvent(event))
        elif event.type() == QEvent.MouseButtonRelease:
            self.mouseReleased.emit(QMouseEvent(event))
        elif event.type() == QEvent.MouseMove:
            self.mousePositionChange.emit(QMouseEvent(event))
        else:
            res = QObject.eventFilter(self,obj, event)
        return res
    

