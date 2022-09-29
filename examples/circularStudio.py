from auxstudio.interface import *
import numpy as np
import pycircularstats.fileIO as pyCfileIO
import pycircularstats.convert as pyCconvert
import pycircularstats.math as pyCmath
import pycircularstats.draw as pyCdraw
import pycircularstats.mouseEventQt as pyCmouseEvent
import PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvas



class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.sceneGrahics = PyQt5.QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.sceneGrahics)
        #pyCdraw.DPIEXPORT = 81
        #print(self.imageicono.geometry())
        #self.imageicono.setPixmap(QtGui.QPixmap('../images/logo.png').scaled(202,191, QtCore.Qt.KeepAspectRatio))
        self.buttonload.clicked.connect(self.load_data)
        self.calculate.clicked.connect(self.exec_func)

        self.type0.setEnabled(True)
        self.type1.setEnabled(True)
        self.type2.setEnabled(True)
        self.labelModules.setEnabled(False)
        self.comboBoxModules.setEnabled(False)
        self.labelAzimuths.setEnabled(False)
        self.comboBoxAzimuths.setEnabled(False)
        self.buttonload.setEnabled(True)
        self.buttonmap.setEnabled(False)
        self.Map.setEnabled(False)

        handler = pyCmouseEvent.mouseEvent(self.graphicsView)
        self.graphicsView.installEventFilter(handler)
        handler.mousePressed.connect(lambda event: self.mousePressEvent(event, 1))
        self.graphicsView.setMouseTracking(True)


    def mousePressEvent(self, event, posMouse=None):
        if posMouse == 1: self.save_data2pc()


    def save_data2pc(self):
        if self.show_image * self.show_text: return
        if self.show_image:
            fileName = QtWidgets.QFileDialog.getSaveFileName(self,self.tr("Export to PNG"), "image", self.tr("PNG image (*.png)"))
            if fileName[0] != "":
                rect = self.sceneGrahics.itemsBoundingRect()
                pixmap = QtGui.QPixmap(int(rect.width()), int(rect.height()))
                painter = QtGui.QPainter(pixmap)
                self.sceneGrahics.render(painter, rect)
                del painter
                pixmap.save(str(fileName[0]) + '.png')
            else:
                pass
        else: # text
            fileName = QtWidgets.QFileDialog.getSaveFileName(self,self.tr("Export to TXT"), "info", self.tr("TXT file (*.txt)"))
            if fileName[0] != "":
                text_file = open(str(fileName[0]) + '.txt', 'w')
                text_file.write(self.sceneGrahics.items()[0].toPlainText())
                text_file.close()
            else:
                pass


    def show_message(self, typeSMS, info):
        msg = PyQt5.QtWidgets.QMessageBox()
        msg.setIcon(PyQt5.QtWidgets.QMessageBox.Information)
        msg.setText(typeSMS)
        msg.setInformativeText(info)
        msg.setWindowTitle(typeSMS + " pyCircStudio")
        msg.exec_()


    def drawObject(self, objectReturn):
        if objectReturn != []:
            self.sceneGrahics.clear()
            try:
                canvas = FigureCanvas(objectReturn)
                canvas.draw()
                size = canvas.size()
                width, height = size.width(), size.height()
                item = QtGui.QPixmap(QtGui.QImage(canvas.buffer_rgba(), width, height, QtGui.QImage.Format_ARGB32).rgbSwapped())
                self.sceneGrahics = QtWidgets.QGraphicsScene()
                self.sceneGrahics.addPixmap(item)
                self.graphicsView.setScene(self.sceneGrahics)
                self.sceneGrahics.update()
                self.show_image = True
                self.show_text  = False
            except: # its text
                self.sceneGrahics.addText(str(objectReturn), QtGui.QFont('Arial Black', 15, QtGui.QFont.Light))
                self.show_image = False
                self.show_text  = True

            self.resizeEvent(None)
        else:
            self.showMessageInView("ERROR: No information wind in region")

    def load_data(self):
        print(self.imageicono.geometry())
        fpath = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            '../datasets',"Image files (*.txt)")[0]
        if fpath:
            if   self.type0.isChecked(): typeF = 'cartesian'
            elif self.type1.isChecked(): typeF = 'incremental'
            elif self.type2.isChecked(): typeF = 'polar'
            elif self.type3.isChecked(): typeF = 'vectors'
            else:
                self.show_message("ERROR", "select type")
            try:
                self.data = pyCfileIO.loaddata(fpath, typedata=typeF)
                self.modules  = self.data[:,0]
                self.azimuths = self.data[:,1]
                self.X_coordinate = self.data[:,2]
                self.Y_coordinate = self.data[:,3]
                fname = fpath.split("/")[-1]
                self.labelpath.setText(fname)
                self.calculate.setEnabled(True)
            except:
                self.show_message("ERROR", "invalid text format")

    def resizeEvent(self, event):
        bounds = self.sceneGrahics.itemsBoundingRect()
        self.graphicsView.fitInView(bounds, QtCore.Qt.KeepAspectRatioByExpanding)
        self.graphicsView.centerOn(0,0)

    def exec_func(self):
        if self.drawmoduleandazimuthdistribution.isChecked():
            self.drawazimuthdistrib()
        elif self.drawdistribution.isChecked():
            self.drawdistrib()
        elif self.drawhistogram.isChecked():
            self.drawhisto()
        elif self.drawPoints.isChecked():
            self.drawpoi()
        elif self.drawdensityMap.isChecked():
            self.drawdenmap()
        elif self.drawqqplot.isChecked():
            self.drawqq()
        elif self.drawVectors.isChecked():
            self.drawvec()
        elif self.modstats.isChecked():
            self.modulestats()
        elif self.azimuthstats.isChecked():
            self.azistats()

    def drawazimuthdistrib(self):
        figure = pyCdraw.drawmoduleandazimuthdistribution(self.X_coordinate, self.Y_coordinate)
        self.drawObject(figure)

    def drawdistrib(self):
        figure = pyCdraw.drawdistribution(self.azimuths)
        self.drawObject(figure)

    def drawhisto(self):
        figure = pyCdraw.drawhistogram(self.azimuths, classSize=15)
        self.drawObject(figure)

    def drawpoi(self):
        figure = pyCdraw.drawPoints(self.X_coordinate, self.Y_coordinate, outlier_percent = 0.08)
        self.drawObject(figure)

    def drawdenmap(self):
        figure = pyCdraw.drawdensityMap(self.X_coordinate, self.Y_coordinate, bandwidth=10, paintpoint = True)
        self.drawObject(figure)

    def drawqq(self):
        figure = pyCdraw.drawqqplot(self.azimuths)
        self.drawObject(figure)
        del figure

    def drawvec(self):
        figure = pyCdraw.drawVectors(self.data)
        self.drawObject(figure)

    def modulestats(self):
        figure = pyCmath.allmodulestatistics(self.modules)
        self.drawObject(figure)

    def azistats(self):
        figure  = pyCmath.allazimuthstatistic(self.azimuths)
        figure += pyCmath.raotest(self.azimuths)
        figure += pyCmath.rayleightest(self.azimuths)
        self.drawObject(figure)


if __name__ == "__main__":
    try:
        app
    except:
        app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    w = window.imageicono.geometry().width()
    h = window.imageicono.geometry().height()
    window.imageicono.setPixmap(QtGui.QPixmap('../images/logo.png').scaled(w,h, QtCore.Qt.KeepAspectRatio))
    app.exec_()
