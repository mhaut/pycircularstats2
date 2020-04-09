#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pycircularstats.convert as pyCconvert



def readfromfile(path):
    vector = [line[:-1].split('\t') for line in open(path, 'r')]
    return np.array(vector).astype("float")


def correct_type(typedata, data_):
    if ((np.min(data_) >= 0) and data_.shape[1] == 2 and typedata == 3):
        return True
    if (data_.shape[1] == 2 and typedata == 2):
        return True
    if (data_.shape[1] == 4 and typedata == 1 or typedata == 4):
        return True
    # not correct
    return False


def loaddata(path, typedata = 2):
    if not path:
        print('error, not path file')
        exit()
    data_ = readfromfile(path)
    if data_.shape[0] > 1:
        if correct_type(typedata, data_) == False:
            print("Error, the file is not of Cartesian coordinates type (type 1).")
            print("Error, the file is not of Incremental data type (type 2).")
            print("Error, the file is not of Polar coordinates type (type 3).")
            exit()
        else:
            res = np.zeros((data_.shape[0], 9))
            if typedata == 1: # probado, ok
                res[:, 4:8] = np.array([data_[:, i] for i in range(4)]).T
                increm              = pyCconvert.tocalculateincr(data_)
                polar_vectors       = pyCconvert.vectors2polar(increm)
                rectangular_vectors = increm
            elif typedata == 2: # probado, ok
                polar_vectors       = pyCconvert.vectors2polar(data_)
                rectangular_vectors = data_
            elif typedata == 3:
                rectangular_vectors   = pyCconvert.vectors2rectangular(data_)
                polar_vectors         = data_
            elif typedata == 4:
                res[:, :4] = np.array([data_[:, i] for i in range(4)]).T
                return res
            res[:,:2] = polar_vectors
            res[:,2:4] = rectangular_vectors
    return res


def text2file(text, pathname):
    f = open(pathname + ".txt", 'w')
    f.write (text)
    f.close()
