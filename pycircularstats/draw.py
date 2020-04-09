#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import pycircularstats.math as pyCmath
import pycircularstats.convert as pyCconvert

# Style sheets reference
#https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html

DPIEXPORT = 150
#STYLE_MATPLOTLIB = "dark_background"
#STYLE_MATPLOTLIB = "seaborn-deep"
STYLE_MATPLOTLIB = "default"


def creategraphicpolar(num_elements, length):
    ax = None
    fig = plt.figure(dpi=DPIEXPORT)
    ax = plt.subplot(111, polar=True)
    ax.grid(True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title("Sample size, n = "+str(num_elements), va='bottom')
    if length != None: ax.set_rlim(0, length)
    for ax in fig.axes:
        ax.margins(0,0)
    return fig, ax


def drawdistribution(azimuths):
    scale_factor = 1
    data_x = list()
    data_y = list()
    his = pyCmath.histogram(azimuths, 1)
    cbase = int(max(his[:,0]) / 33) + 1       # number of elements for each point in the plot
    d1 = 21
    length = 23.5 + 1		# fixed circumference radius and plot width and heigth

    for i in range(360):
        h = int(his[i,0] / float(cbase))  # elements/point as a function of absolute frequency of 10 classes
        if h > 0:
            for g in range(h):
                radian = np.radians(90 - i)
                x = np.cos(radian) * (d1 - ((d1 * 0.025) * g))
                y = np.sin(radian) * (d1 - ((d1 * 0.025) * g))
                data_x.append(x)
                data_y.append(y)
    n, module, theta, _ = pyCconvert.getpolarvalues(scale_factor,np.array(data_x),np.array(data_y))
    fig, ax = creategraphicpolar(n, length)
    ax.plot(theta,module,'o', color='b',markersize=5)
    azimuth = pyCmath.averageazimuth(azimuths)
    radian = np.radians(90 - azimuth)
    x = np.cos(radian) * (d1 + (d1 * 0.1))
    y = np.sin(radian) * (d1 + (d1 * 0.1))
    vm = pyCmath.vonmisesparameter(azimuths)
    if vm >= 0.9:
        ax.annotate("",
                    xy=(np.arctan2(x, y), np.sqrt(x**2 + y**2)), xycoords='data',
                    xytext=(0, 0), textcoords='data',
                    arrowprops=dict(arrowstyle="->, head_width=1, head_length=1",
                                    connectionstyle="arc3",edgecolor='red',
                                    linewidth = 3))
    else:
        print("Concentration is low, the mean azimuth is not drawn")
    # confidence interval
    if vm >= 0.9:
        module = pyCmath.meanmodule(azimuths)
        ci = pyCmath.confidenceinterval(n, azimuth, module, vm)
        xmin = np.cos(np.radians(90 - ci[0])) * (d1 + (d1 * 0.1))
        xmax = np.cos(np.radians(90 - ci[1])) * (d1 + (d1 * 0.1))
        ymin = np.sin(np.radians(90 - ci[0])) * (d1 + (d1 * 0.1))
        ymax = np.sin(np.radians(90 - ci[1])) * (d1 + (d1 * 0.1))
        dmin = np.array([xmin, xmax])
        dmax = np.array([ymin, ymax])
        module = np.sqrt(dmin**2 + dmax**2)
        theta = np.arctan2(dmin, dmax)
        ax.plot(theta,module,'o', color='r',markersize=5)
        vertices = [
            (theta[0],module[0]),
            (np.mean(theta),np.mean(module)),
            (theta[1],module[1]),
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE3,
            Path.CURVE3,
        ]
        path = Path(vertices, codes)
        patch = patches.PathPatch(path,facecolor='none',edgecolor='red',lw=1)
        ax.add_patch(patch)
    return ax.get_figure()


def drawmoduleandazimuthdistribution(data_x, data_y):
    # Plots a graphic of all the vectors from a common origin (0,0)
    #
    # Args:
    #   data_x : vector components (increments) over the X axis
    #   data_y : vector components (increments) over the Y axis
    #
    # Returns:
    #   Plot the graphic and/or save the graphic as SVG
    #
    num_data = data_x.shape[0]
    module   = np.sqrt(data_x**2 + data_y**2)
    theta    = np.arctan2(data_x, data_y)
    length_  = np.max(module) + 10

    with plt.style.context(STYLE_MATPLOTLIB):
        avg = np.average
        fig, ax = creategraphicpolar(data_x.shape[0], length_)
        for dx,dy in zip(theta, module):
            ax.annotate("",
            xy=(dx, dy), xycoords='data',
            xytext=(0.0, 0.0), textcoords='data',
            arrowprops=dict(arrowstyle="->, head_width=0.3, head_length=0.3",
                            connectionstyle="arc3",edgecolor='blue',
                            linewidth = 1
                            ),
            )
        avg = np.average
        ax.annotate("",
                    xy=(np.arctan2(avg(data_x), avg(data_y)), \
                        np.sqrt(avg(data_x)**2 + avg(data_y)**2)), \
                    xycoords='data', xytext=(0, 0), textcoords='data',
                    arrowprops=dict(arrowstyle="->, head_width=1, head_length=1",
                    connectionstyle="arc3",edgecolor='red', linewidth = 2.5))
    return ax.get_figure()


def drawhistogram(azimuths, classSize = 15, changeStype=True):
    his  = pyCmath.histogram(azimuths, classSize)
    max_ = max(his[:, 1]) * 105
    d1 = round(max_)
    length_ = d1 * 1.2

    theta = np.linspace(0.0, 2 * np.pi, his.shape[0], endpoint=False)
    radii = his[:,1] * 100
    width = (2*np.pi) / his.shape[0]
    
    with plt.style.context('dark_background'):
        fig, ax = creategraphicpolar(azimuths.shape[0], length_)
        bars = ax.bar(theta, radii, width=width, bottom=0.0)
        if changeStype:
            for r, bar in zip(radii, bars):
                bar.set_facecolor(plt.cm.jet(r / radii.size))
                bar.set_alpha(0.8)
        else:
            for r, bar in zip(radii, bars):
                bar.set_facecolor([0.20, 0.6, 0.8]) # RGB color
                bar.set_alpha(0.8)
        vm = pyCmath.vonmisesparameter(azimuths)
        if vm >= 0.53:
            azimuth = pyCmath.averageazimuth(azimuths)
            x = np.cos(np.radians(90 - azimuth)) * (d1 * 1.1)
            y = np.sin(np.radians(90 - azimuth)) * (d1 * 1.1)
            ax.annotate("",
                        xy=(np.arctan2(x, y), np.sqrt(x**2 + y**2)), xycoords='data',
                        xytext=(0.0, 0.0), textcoords='data',
                        arrowprops=dict(arrowstyle="->, head_width=1, head_length=1",
                                        connectionstyle="arc3",edgecolor='red',
                                        linewidth = 3))
        else:
            print("Concentration is low, the mean azimuth is not drawn")
    return ax.get_figure()


def drawPoints(data_x, data_y, outlier_percent = 0.05):
    assert outlier_percent < 1
    scale_factor = 1
    module = np.sqrt(data_x**2 + data_y**2)
    theta = np.arctan2(data_x,data_y)
    maxlen = np.max(module) + 10
    cant = int(module.shape[0] * outlier_percent)
    inds = np.argsort(-module)
    module = -np.sort(-module)
    theta = theta[inds]

    with plt.style.context(STYLE_MATPLOTLIB):
        fig, ax = creategraphicpolar(data_x.shape[0], maxlen)
        ax.plot(theta[cant:],module[cant:],'o', color='b',markersize=5)
        ax.plot(theta[:cant],module[:cant],'o', color='r',markersize=5)
    return ax.get_figure()


def drawdensityMap(data_x, data_y, outlier_percent = 0.05, paintpoint = False,
                    bandwidth = 20, harmonicmean = False):

    x, y, z = pyCmath.kde2D(data_x, data_y, bandwidth)

    fig, ax = plt.subplots(1,1, dpi=DPIEXPORT)
    plt.set_cmap('jet')
    ax.set_title("Density map\nSample size, n = "+str(data_x.shape[0]), va='bottom')
    cb = plt.colorbar(ax.pcolor(x,y,z))
    cb.ax.set_ylabel('Probability density')

    if paintpoint:
        harmonicmean = False
        data = np.stack((data_x, data_y), axis=1)
        Vec = pyCmath.allharmonicMean(data).reshape(-1) if harmonicmean \
            else pyCconvert.vectors2polar(data)[:,0]
        # efficient order
        data = data[np.argsort(Vec)]
        cant = int(data_x.shape[0] * outlier_percent)
        ax.plot(data[:-cant,0],data[:-cant,1],'o', mfc='black',mec='k')
        ax.plot(data[-cant:,0],data[-cant:,1],'o', mfc='red',mec='k')
    return ax.get_figure()


def drawVectors(data,scaleVector=None):
    xini = data[:,0]
    yini = data[:,1]
    xfin = data[:,2]
    yfin = data[:,3]

    if scaleVector != None:
        xaux = xfin - xini
        yaux = yfin - yini
        xaux *= scaleVector
        yaux *= scaleVector
        xfin = xaux + xini
        yfin = yaux + yini

    xmin = min(np.min(xini), np.min(xfin))
    xmax = max(np.max(xini), np.max(xfin))
    ymin = min(np.min(yini), np.min(yfin))
    ymax = max(np.max(yini), np.max(yfin))

    with plt.style.context(STYLE_MATPLOTLIB):
        fig = plt.figure(dpi = DPIEXPORT)
        ax = fig.add_subplot(111)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        for i in range(len(xini)):
            valueScale = 0.3
            style = "->, head_width="+str(valueScale)+", head_length="+str(valueScale)
            ax.annotate("",
            xy=(xfin[i], yfin[i]), xycoords='data',
            xytext=(xini[i], yini[i]), textcoords='data',
            arrowprops=dict(arrowstyle=style,
                            connectionstyle="arc3",edgecolor='red',
                            linewidth = 1,
                            ),
            )
        ax.set_title("Sample size, n = "+str(len(xini)), va='bottom')
    return ax.get_figure()


def drawqqplot(azimuths):
    percent = int(azimuths.shape[0] * 20 / 100)
    sort_vectors = np.radians(np.sort(azimuths))
    v = sort_vectors / (2*np.pi)
    x = np.zeros((2,azimuths.shape[0]))
    x[1,: ] = v
    x[0,: ] = np.arange(1,azimuths.shape[0]+1) / float(azimuths.shape[0] + 1)
    y = np.zeros((2, 2 * percent))

    y[1, :percent] = v[:percent] + 1
    y[1, percent:2*percent] = v[azimuths.shape[0]-percent:azimuths.shape[0]] - 1

    y[0,:percent] = x[0,:percent] + 1
    y[0, percent:2*percent] = x[0, azimuths.shape[0]-percent:azimuths.shape[0]]-1

    z = np.vstack((x.T,y.T))
    z = np.array(sorted(z, key=lambda a_entry: a_entry[1]))

    with plt.style.context(STYLE_MATPLOTLIB):
        fig = plt.figure(dpi = DPIEXPORT)
        ax = fig.add_subplot(111)
        ax.set_title("QQ plot")
        ax.grid(True)
        ax.plot(z[:,0],z[:,1],'o')
    return ax.get_figure()

