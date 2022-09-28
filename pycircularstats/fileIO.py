#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pycircularstats.convert as pyCconvert


def readfromfile(path):
    return np.loadtxt(path, delimiter='\t')

def correct_type(typedata, data):
    if   typedata == 'cartesian' and data.shape[1] == 4: return True
    elif typedata == 'polar' and data.shape[1] == 2 and np.min(data) >= 0: return True
    elif typedata == 'incremental' and data.shape[1] == 2: return True
    elif typedata == 'vectors' and data.shape[1] == 4: return True
    else: return False # not correct

def data2res(typedata, data):
    res = np.zeros((data.shape[0], 9))
    if typedata == 'cartesian':
        res[:, 4:8] = np.array([data[:, i] for i in range(4)]).T
        rectangular_vectors = pyCconvert.tocalculateincr(data)
        polar_vectors       = pyCconvert.vectors2polar(rectangular_vectors)
    elif typedata == 'incremental':
        rectangular_vectors = data
        polar_vectors       = pyCconvert.vectors2polar(data)
    elif typedata == 'polar':
        polar_vectors       = data
        rectangular_vectors = pyCconvert.vectors2rectangular(data)
        #print(rectangular_vectors)
        #exit()
    elif typedata == 'vectors':
        res[:, :4] = np.array([data[:, i] for i in range(4)]).T
        return res
    res[:,:2]  = polar_vectors
    res[:,2:4] = rectangular_vectors
    return res

def loaddata(path, typedata = 'incremental'):
    if not path:
        print('error, not path file')
        return None
    data = readfromfile(path)
    if data.shape[0] > 1:
        TYPES_AVAIL = ['cartesian', 'incremental', 'polar', 'vectors']
        if typedata.lower() not in TYPES_AVAIL:
            print("Error, format selected is not avaiable")
            print(TYPES_AVAIL)
            return None
        elif correct_type(typedata, data) == False:
            print("Error, the file is not in the correct format.")
            return None
        else:
            return data2res(typedata, data)
    else:
        print("Error, in read file, check it!")
        return None


def text2file(text, pathname):
    f = open(pathname + ".txt", 'w')
    f.write (text)
    f.close()
