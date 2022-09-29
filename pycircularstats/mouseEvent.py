from qgis.PyQt.QtGui import QMouseEvent
from qgis.PyQt.QtCore import QObject,QEvent,pyqtSignal, Qt


class mouseEvent(QObject):
    mouseDoubleClicked  = pyqtSignal(QMouseEvent)
    mousePressed        = pyqtSignal(QMouseEvent)
    mouseReleased       = pyqtSignal(QMouseEvent)
    mousePositionChange = pyqtSignal(QMouseEvent)
    def __init__(self,parent=None):
        QObject.__init__(self,parent=parent)

    def eventFilter(self, obj=QObject, event=QEvent):
        res=True
        if   event.type() == QEvent.Type.MouseButtonDblClick:
            self.mouseDoubleClicked.emit(QMouseEvent(event))
        elif event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.mousePressed.emit(QMouseEvent(event))
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleased.emit(QMouseEvent(event))
        elif event.type() == QEvent.Type.MouseMove:
            self.mousePositionChange.emit(QMouseEvent(event))
        else:
            res = QObject.eventFilter(self,obj, event)
        return res

#if event.button() == QtCore.Qt.LeftButton:
