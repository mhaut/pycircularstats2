#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np



def vectors2rectangular(vectors):
    #rectangular_vectors = vectors
    rectangular_vectors = np.zeros((vectors.shape))
    grades = vectors[:,1]
    module = vectors[:,0]
    radians = np.radians(grades)
    x1 = np.sin(radians) * module
    y1 = np.cos(radians) * module
    rectangular_vectors[:,0] = x1
    rectangular_vectors[:,1] = y1
    return rectangular_vectors


#def vectors2rectangular(vectors, init=1):
    #rectangular_vectors = np.zeros((vectors.shape))
    #module  = vectors[:, 0]
    #grades  = vectors[:, 1]
    #val1 = np.degrees(np.cos(np.radians(grades))) * module # x
    #val2 = np.degrees(np.sin(np.radians(grades))) * module # y
    ##print(va1)
    ##print(np.degrees(np.cos(grades)*module))
    ##exit()
    #rectangular_vectors[:, 0] = val1 if init == 0 else val2
    #rectangular_vectors[:, 1] = val2 if init == 0 else val1
    #return rectangular_vectors

#def vectors2rectangularMAP(module, grades):
    #rectangular_vectors = []
    #rectangular_vectors.append(np.cos(np.radians(grades)) * module)
    #rectangular_vectors.append(np.sin(np.radians(grades)) * module)
    #return rectangular_vectors

def vectors2rectangularMAP(modules, grades, init=1):
    rectangular_vectors = np.ones((len(modules), 2))
    val1 = np.degrees(np.cos(np.radians(grades))) * modules # x
    val2 = np.degrees(np.sin(np.radians(grades))) * modules # y
    rectangular_vectors[:, 0] = val1 if init == 0 else val2
    rectangular_vectors[:, 1] = val2 if init == 0 else val1
    return rectangular_vectors

#def vectors2polar(vectors):
    #num_data = vectors.shape[0]
    #x = vectors[:,0]
    #y = vectors[:,1]
    #module = np.sqrt(x**2 + y**2)
    ##grades = np.degrees(np.arctan2(y,x))
    #grades = np.degrees(np.arctan2(y,x))
    ##grades = np.degrees(np.arctan2(x,y))
    ##grades = np.degrees(np.arctan(x/y))
    #grades[grades<0] += 360
    #polar_vectors = np.array([module, grades]).T
    #return polar_vectors

def vectors2polar(vectors, posX=0):
    x = vectors[:,0]
    y = vectors[:,1]
    module = np.sqrt(x**2 + y**2)
    grades = np.degrees(np.arctan2(x,y))
    grades[grades<0] += 360
    polar_vectors = np.array([module, grades]).T
    return polar_vectors

def getpolarvalues(scale, data_x, data_y):
    [module, theta] = vectors2polar(np.stack((data_x, data_y), axis=1)).T
    max_   = np.max(module) + 1  
    angle_ticks = [np.round(max_ * scale * a) for a in np.arange(0.25, 1.01, 0.25)][::-1]
    return data_x.shape[0], module, theta, np.array(angle_ticks)


def tocalculateincr(matrix):
    num_elements = matrix.shape[0]
    x_coordinates = matrix[:,0] - matrix[:,2]
    y_coordinates = matrix[:,1] - matrix[:,3]
    incr = np.column_stack((x_coordinates, y_coordinates))
    incr = np.reshape(np.array(incr), (num_elements, 2))
    return incr
