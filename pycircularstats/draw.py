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

DPIEXPORT = 120
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
    his = pyCmath.histogram(azimuths, 1)[:,0]
    cbase = (np.max(his) / 33) + 1.8       # number of elements for each point in the plot
    d1 = 21

    fig, ax = creategraphicpolar(len(azimuths), d1*1.2)

    for i in range(359):
        h = his[i+1] / cbase  # elements/point as a function of absolute frequency of 10 classes
        if h > 0:
            for g in range(int(h)+1):
                radian = np.radians(90-i)
                x = np.cos(radian) * (d1 - ((d1 * 0.025) * g))
                y = np.sin(radian) * (d1 - ((d1 * 0.025) * g))
                data_x.append(x)
                data_y.append(y)
    data_x = np.array(data_x)
    data_y = np.array(data_y)
    n, module, theta, _ = pyCconvert.getpolarvalues(scale_factor, np.array(data_x), np.array(data_y))
    theta = np.radians(theta)
    ax.scatter(theta, module, color='b', s=3)

    azimuth = pyCmath.averageazimuth(azimuths)
    radian = np.radians(azimuth)
    x = np.cos(radian) * (d1 + (d1 * 0.1))
    y = np.sin(radian) * (d1 + (d1 * 0.1))
    vm = pyCmath.vonmisesparameter(azimuths)
    if vm >= 0.9:
        ax.annotate("",
                    xy=(np.arctan2(y,x), np.sqrt(x**2 + y**2)), xycoords='data',
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
    #module   = np.sqrt(data_x**2 + data_y**2)
    #theta    = np.arctan2(data_x,data_y)
    #theta    = np.arctan2(data_y, data_x)
    [module, theta] = pyCconvert.vectors2polar(np.stack((data_x, data_y), axis=1)).T
    #theta    = np.arctan(np.average(np.sin(np.radians(azimuths))) / np.average(np.cos(np.radians(azimuths))))
    length_  = np.max(module)

    with plt.style.context(STYLE_MATPLOTLIB):
        avg = np.average
        fig, ax = creategraphicpolar(data_x.shape[0], length_*1.2)
        print(np.unique(theta, return_counts=1))
        for dx,dy in zip(np.radians(theta), module):
            ax.annotate("",
            xy=(dx, dy), xycoords='data',
            xytext=(0.0, 0.0), textcoords='data',
            arrowprops=dict(arrowstyle="->, head_width=0.3, head_length=0.3",
                            connectionstyle="arc3",edgecolor='blue',
                            linewidth = 1
                            ),
            )
            #ax.plot((0, dx), (0, dy), color='blue', linewidth=2, zorder=3)
            #ax.arrow(0,0,dx,dy)
        avg = np.average
        arrv = np.sqrt(avg(data_x)**2 + avg(data_y)**2)
        arrv /= (length_*0.25)
        arrv = 1 if arrv*2>1 else arrv
        lwid = np.min([2.5, arrv * 5])
        #print("-----", (np.arctan2(avg(data_x), avg(data_y)), np.sqrt(avg(data_x)**2 + avg(data_y)**2)))
        ###ax.annotate("",
                    ###xy=(np.arctan2(avg(data_y), avg(data_x)), \
                        ###np.sqrt(avg(data_x**2) + avg(data_y**2))), \
                    ###xycoords='data', xytext=(0, 0), textcoords='data',
                    ####arrowprops=dict(arrowstyle="->, head_width=0.3, head_length=0.3",
                    ####connectionstyle="arc3",edgecolor='red', linewidth = 2))
                    ###arrowprops=dict(arrowstyle="->, head_width="+str(arrv)+", head_length="+str(arrv),
                    ###connectionstyle="arc3",edgecolor='red', linewidth = lwid))
        #print("np.average(theta)", np.average(theta))
        ax.annotate("",
                    xy=(np.radians(pyCmath.averageazimuth(theta)), np.average(module)),
                        xycoords='data', xytext=(0, 0), textcoords='data',
                        arrowprops=dict(arrowstyle="->, head_width="+str(arrv)+", head_length="+str(arrv),
                                        connectionstyle="arc3",edgecolor='red', linewidth = lwid))
        #dx = np.arctan2(avg(data_y), avg(data_x))
        #dy = np.sqrt(avg(data_x)**2 + avg(data_y)**2)
        #ax.plot((0, dx), (0, dy), color='red', linewidth=2, zorder=3)
        #ax.arrow(0,0,dx,dy)
    return ax.get_figure()


def drawhistogram(azimuths, classSize = 15, changeStype=True):
    his  = pyCmath.histogram(azimuths, classSize)
    d1 = round(max(his[:, 1]) * 105)

    theta = np.linspace(0.0, 2 * np.pi, his.shape[0], endpoint=False)
    radii = his[:,1] * 100
    width = (2*np.pi) / his.shape[0]
    
    with plt.style.context(STYLE_MATPLOTLIB):
        fig, ax = creategraphicpolar(azimuths.shape[0], d1)
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
            if d1 < np.sqrt(x**2 + y**2): ax.set_rlim(0, np.sqrt(x**2 + y**2)+1.1)
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
    #module = np.sqrt(data_x**2 + data_y**2)
    #theta = np.arctan2(data_x, data_y)
    #theta = np.arctan2(data_y, data_x)
    [module, theta] = pyCconvert.vectors2polar(np.stack((data_x, data_y), axis=1)).T
    theta = np.radians(theta)
    cant = int(module.shape[0] * outlier_percent)
    inds = np.argsort(-module)
    module = -np.sort(-module)
    theta = theta[inds]
    with plt.style.context(STYLE_MATPLOTLIB):
        fig, ax = creategraphicpolar(data_x.shape[0], np.max(module) * 1.2)
        ax.plot(theta[cant:],module[cant:],'o', color='b', markersize=3)
        ax.plot(theta[:cant],module[:cant],'o', color='r', markersize=3)
    return ax.get_figure()


def drawdensityMap(data_x, data_y, outlier_percent = 0.05, paintpoint = False,
                    bandwidth = 20, harmonicmean = False):
    x, y, z = pyCmath.kde2D(data_x, data_y, bandwidth)
    if paintpoint:
        harmonicmean = False
        data = np.stack((data_x, data_y), axis=1)
        if harmonicmean: Vec = pyCmath.allharmonicMean(data).reshape(-1)
        else: Vec = pyCconvert.vectors2polar(data)[:,0]
        # efficient order
        data = data[np.argsort(Vec)]
        cant = int(data_x.shape[0] * outlier_percent)

    with plt.style.context(STYLE_MATPLOTLIB):
        fig, ax = plt.subplots(1,1, dpi=DPIEXPORT)
        plt.set_cmap('jet')
        ax.set_title("Density map\nSample size, n = "+str(data_x.shape[0]), va='bottom')
        cb = plt.colorbar(ax.pcolor(x,y,z))
        cb.ax.set_ylabel('Probability density')
        if paintpoint:
            ax.plot(data[:-cant,0],data[:-cant,1],'o', mfc='lightblue',mec='k', markersize=5)
            ax.plot(data[-cant:,0],data[-cant:,1],'o', mfc='firebrick',mec='k', markersize=5)
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
        ax.set_xlim(np.min(z[:,0])*1.1, np.max(z[:,0])*1.1)
        ax.set_ylim(np.min(z[:,1])*1.1, np.max(z[:,1])*1.1)
    return ax.get_figure()


def drawVectors(vectors, scaleVector=None, zoomed_points=[]):
    if np.sum(np.abs(vectors)) == 0: return None
    xini = vectors[:,0]; yini = vectors[:,1]
    xfin = vectors[:,2]; yfin = vectors[:,3]
    #xfin = data[:,2]*1.0001; yfin = data[:,3]*1.0001
    xmin = min(np.min(xini), np.min(xfin))
    xmax = max(np.max(xini), np.max(xfin))
    ymin = min(np.min(yini), np.min(yfin))
    ymax = max(np.max(yini), np.max(yfin))
    with plt.style.context(STYLE_MATPLOTLIB):
        fig = plt.figure(dpi = DPIEXPORT)
        ax = fig.add_subplot(111)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        for i in range(len(vectors[:,0])):
            valueScale = 0.2
            style = "->, head_width="+str(valueScale)+", head_length="+str(valueScale)
            ax.annotate("",
            xy=(xfin[i], yfin[i]), xycoords='data',
            xytext=(xini[i], yini[i]), textcoords='data',
            arrowprops=dict(arrowstyle=style,
                            connectionstyle="arc3",edgecolor='red',
                            linewidth = 1,
                            ),
            )
    if zoomed_points:
        listapoints = vectors[zoomed_points,:4]
        print(listapoints)
        x1 = np.min(listapoints[:,[0,2]]); x2 = np.max(listapoints[:,[0,2]])
        y1 = np.min(listapoints[:,[1,3]]); y2 = np.max(listapoints[:,[1,3]])
        from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
        axins = zoomed_inset_axes(ax, 30, loc=2, borderpad=1) # zoom-factor: 2.5, location: upper-left
        mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
        #x1, x2, y1, y2 = 726045, 726060, 4372710, 4372757 # specify the limits
        axins.set_xlim(x1, x2) # apply the x-limits
        axins.set_ylim(y1, y2) # apply the y-limits
        plt.yticks(visible=False)
        plt.xticks(visible=False)

        for i in zoomed_points:
            valueScale = 0.2
            style = "->, head_width="+str(valueScale)+", head_length="+str(valueScale)
            axins.annotate("",
            xy=(xfin[i], yfin[i]), xycoords='data',
            xytext=(xini[i], yini[i]), textcoords='data',
            arrowprops=dict(arrowstyle=style,
                            connectionstyle="arc3",edgecolor='blue',
                            linewidth = 1,
                            ),
            )
    ax.set_title("Sample size, n = "+str(len(vectors[:,0])), va='bottom')

    return ax.get_figure()
