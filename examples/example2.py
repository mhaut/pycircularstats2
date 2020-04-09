import pycircularstats.fileIO as pyCfileIO
import pycircularstats.convert as pyCconvert
import pycircularstats.math as pyCmath
import pycircularstats.draw as pyCdraw


def test():
    path = '../examples/datasets/RectangularData.txt'
    data = pyCfileIO.loaddata(path, typedata=2)
    azimuths = data[:,1]
    X_coordinate = data[:,2]
    Y_coordinate = data[:,3]
    scale_factor = 1
    num_data, module, theta, angle_ticks = pyCconvert.getpolarvalues(scale_factor, X_coordinate, Y_coordinate)
    n_classes = 1
    histo = pyCmath.histogram(azimuths, n_classes)
    path = '../examples/datasets/otros/datos4polar.txt'
    data = pyCfileIO.loaddata(path, typedata=3)
    rec_vectors = pyCconvert.vectors2rectangular(data)
    
    path = '../examples/datasets/RectangularData.txt'
    data = pyCfileIO.loaddata(path, typedata=2)
    pyCmath.allmodulestatistics(data[:,0])
    pyCmath.allazimuthstatistic(data[:,1])
    pyCmath.raotest(data[:,1])
    pyCmath.rayleightest(data[:,1])
    
    path = '../examples/datasets/RectangularData.txt'
    data = pyCfileIO.loaddata(path, typedata=2)
    azimuths = data[:,1]
    X_coordinate = data[:,2]
    Y_coordinate = data[:,3]
    #pyCdraw.drawpoints(X_coordinate, Y_coordinate, percentageoutliers = 5)
    pyCdraw.drawdistribution(azimuths)
    # # drawmoduleandazimuthdistribution(X_coordinate, Y_coordinate, saveFile = False)
    
    # # drawhistogram(azimuths)
    # # drawpoints(X_coordinate, Y_coordinate, percentageoutliers = 5, saveFile = False)



def main():
    test()

if __name__ == '__main__':
    main()
