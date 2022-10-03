import matplotlib.pyplot as plt
import pycircularstats.fileIO as pyCfileIO
import pycircularstats.convert as pyCconvert
import pycircularstats.math as pyCmath
import pycircularstats.draw as pyCdraw
import numpy as np


def main():
    for fname, typeD in zip(['MeasuredRealData','RectangularData'],['cartesian', 'incremental']):
        path = '../datasets/'+fname+'.txt'
        data = pyCfileIO.loaddata(path, typedata=typeD)

        modules = data[:,0]
        azimuths = data[:,1]
        values = pyCmath.allmodulestatistics(data[:,0], ndig = 4)
        print(values)
        values = pyCmath.allazimuthstatistic(data[:,1], ndig = 4)
        print(values)
        values = pyCmath.raotest(azimuths)
        print(values)
        values = pyCmath.rayleightest(azimuths)
        print(values)
        X_coordinate = data[:,2]
        Y_coordinate = data[:,3]
        pyCdraw.drawmoduleandazimuthdistribution(X_coordinate, Y_coordinate)
        plt.show()
        pyCdraw.drawdistribution(azimuths)
        plt.show()
        pyCdraw.drawhistogram(azimuths, classSize=15)
        plt.show()
        pyCdraw.drawPoints(X_coordinate, Y_coordinate, outlier_percent = 0.08)
        plt.show()
        exit()
        pyCdraw.drawdensityMap(X_coordinate, Y_coordinate, bandwidth=10, paintpoint = True)
        plt.show()
        pyCdraw.drawqqplot(azimuths)
        plt.show()


if __name__ == '__main__':
    main()
