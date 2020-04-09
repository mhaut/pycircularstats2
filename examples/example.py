import pycircularstats.fileIO as pyCfileIO
import pycircularstats.convert as pyCconvert
import pycircularstats.math as pyCmath
import pycircularstats.draw as pyCdraw
import numpy as np


def test():
    path = '../datasets/RectangularData.txt'
    data = pyCfileIO.loaddata(path, typedata=2)
    modules = data[:,0]
    azimuths = data[:,1]
    pyCmath.allmodulestatistics(data[:,0], ndig = 4)
    pyCmath.allazimuthstatistic(data[:,1], ndig = 4)
    pyCmath.raotest(azimuths)
    pyCmath.rayleightest(azimuths)
    X_coordinate = data[:,2]
    Y_coordinate = data[:,3]
    pyCdraw.drawmoduleandazimuthdistribution(X_coordinate, Y_coordinate)
    pyCdraw.drawdistribution(azimuths)
    pyCdraw.drawhistogram(azimuths, classSize=15)
    pyCdraw.drawPoints(X_coordinate, Y_coordinate, outlier_percent = 0.08)
    pyCdraw.drawdensityMap(X_coordinate, Y_coordinate, bandwidth=10, paintpoint = True)
    pyCdraw.drawqqplot(azimuths)
    pyCdraw.drawVectors(data)


def main():
    test()

if __name__ == '__main__':
    main()
