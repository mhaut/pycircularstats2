#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np



def vectors2rectangular(vectors):
    res = np.zeros((vectors.shape[0],9))
    rectangular_vectors = vectors
    module  = vectors[:, 0]
    grades  = vectors[:, 1]
    rectangular_vectors[:, 0] = np.sin(np.radians(grades)) * module
    rectangular_vectors[:, 1] = np.cos(np.radians(grades)) * module
    return rectangular_vectors


def vectors2polar(vectors):
    num_data = vectors.shape[0]
    x = vectors[:,0]
    y = vectors[:,1]
    module = np.sqrt(x**2 + y**2)
    grades = np.degrees(np.arctan2(x,y))
    grades[grades<0] += 360
    polar_vectors = np.array([module, grades]).T
    return polar_vectors


def getpolarvalues(scale, data_x, data_y):
    module = np.sqrt(data_x**2 + data_y**2)
    theta  = np.arctan2(data_x,data_y)
    max_   = np.max(module) + 1  
    angle_ticks = [np.round(max_ * scale * a) for a in np.arange(0.25, 1.01, 0.25)][::-1]
    return data_x.shape[0], module, theta, np.array(angle_ticks)


def tocalculateincr(matrix):
    num_elements = matrix.shape[0]
    x_coordinates = matrix[:,2] - matrix[:,0]
    y_coordinates = matrix[:,3] - matrix[:,1]
    incr = np.column_stack((x_coordinates, y_coordinates))
    incr = np.reshape(np.array(incr), (num_elements, 2))
    return incr
