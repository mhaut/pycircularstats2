#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.stats as sp_stats
from sklearn.neighbors import KernelDensity


def histogram(vectors, n_classes):
    n_classes = 360 // n_classes
    abs_his = np.zeros(n_classes)
    n_vectors = vectors.shape[0]
    for i in range(n_vectors):
        portion = (vectors[i] * n_classes) / 360.0
        abs_his[int(portion)] += 1
    rel_his = abs_his / float(n_vectors)
    return np.hstack((abs_his.reshape(n_classes,1), rel_his.reshape(n_classes,1)))


#https://en.wikipedia.org/wiki/Circular_mean
def averageazimuth(azimuths):
    print("azimuth degrees", azimuths)
    radians = np.radians(azimuths)
    sin_ = np.average(np.sin(radians))
    cos_ = np.average(np.cos(radians))
    azimuth = np.arctan(sin_/cos_)
    print("azimuth", azimuth)
    #azimuth = np.degrees(azimuth)
    if sin_ > 0 and cos_ > 0:
        pass
    elif cos_ < 0:
        azimuth += np.pi
    elif sin_ < 0 and cos_ > 0:
        azimuth += (2*np.pi)
    return np.degrees(azimuth)

def vonmisesparameter(azimuths):
    n_elements   = azimuths.shape[0]
    mean_module = meanmodule(azimuths)
    if mean_module < 0.53:
        parameter = 2*mean_module + np.power(mean_module,3) + 5*np.power(mean_module,5)/float(6)
    elif mean_module >= 0.53 and mean_module < 0.85:
        parameter = -0.4 + (1.39 * mean_module) + (0.43/float(1 - mean_module))
    elif mean_module >= 0.85:
        parameter = 1/(np.power(mean_module,3) - (4 * np.power(mean_module,2)) + 3 * mean_module)
    # correction for small samples
    if n_elements < 16:
        if parameter < 2:
            parameter = max(parameter - 2/float(n_elements * parameter), 0)
        else:
            parameter = np.power(n_elements - 1,3) * parameter / float(np.power(n_elements - 1,3) + n_elements)
    return parameter


def meanmodule(azimuths):
    azimuths    = np.radians(azimuths)
    sin_        = np.sum(np.sin(azimuths))
    cos_        = np.sum(np.cos(azimuths))
    module      = np.sqrt(np.power(sin_,2) + np.power(cos_,2))
    mean_module = module / azimuths.shape[0]
    return(mean_module)


def confidenceinterval(n, mean_azimuth, mean_module, von_mises):
    z = 1.96
    vm = 1/(np.sqrt(n * von_mises * mean_module))
    ci1 = mean_azimuth + np.degrees(np.arcsin(z * vm))
    ci2 = mean_azimuth - np.degrees(np.arcsin(z * vm))
    return [ci1, ci2]


def circularvariance(azimuths):
    return 1.0 - meanmodule(azimuths)


def circularstandarddeviation(azimuths):
    variance = circularvariance(azimuths)
    deviation = np.sqrt(-2 * np.log(1 - variance))
    return deviation


def circulardispersal(azimuths):
    n   = azimuths.shape[0]
    CSub2 = (1/float(n)) * np.sum(np.cos(2 * np.radians(azimuths)))
    SSub2 = (1/float(n)) * np.sum(np.sin(2 * np.radians(azimuths)))
    RSub2 = np.sqrt((np.power(CSub2,2) + np.power(SSub2,2)))
    R = meanmodule(azimuths)
    result = (1 - RSub2)/float(2 * (np.power(R,2)))
    return result


def skewnessazimuthcoefficient(azimuths):
    n_elements   = azimuths.shape[0]
    sin_ = np.sum(np.sin(np.radians(azimuths)))
    cos_ = np.sum(np.cos(np.radians(azimuths)))
    CSub2 = (1/float(n_elements)) * np.sum(np.cos(2 * np.radians(azimuths)))
    SSub2 = (1/float(n_elements)) * np.sum(np.sin(2 * np.radians(azimuths)))
    RSub2 = np.sqrt((np.power(CSub2,2) + np.power(SSub2,2)))
    R = meanmodule(azimuths)
    azimuthSub2 = np.arctan(SSub2/float(CSub2))
    if SSub2 > 0 and CSub2 > 0:
        pass
    elif SSub2 > 0 and CSub2 < 0:
        azimuthSub2 += np.pi
    elif SSub2 < 0 and CSub2 > 0:
        azimuthSub2 += 2 * np.pi
    elif SSub2 < 0 and CSub2 < 0:
        azimuthSub2 += np.pi
    result = (RSub2 * np.sin(azimuthSub2 - 2 * np.arctan(sin_/float(cos_))))\
                /float(np.power(1-R,1.5))
    return result


def kurtosisazimuthcoefficient(azimuths):
    n_elements   = azimuths.shape[0]
    sin_ = np.sum(np.sin(np.radians(azimuths)))
    cos_ = np.sum(np.cos(np.radians(azimuths)))
    CSub2 = (1/float(n_elements)) * np.sum(np.cos(2 * np.radians(azimuths)))
    SSub2 = (1/float(n_elements)) * np.sum(np.sin(2 * np.radians(azimuths)))
    RSub2 = np.sqrt((np.power(CSub2,2) + np.power(SSub2,2)))
    R = meanmodule(azimuths)
    azimuthSub2 = np.arctan(SSub2/float(CSub2))
    if SSub2 > 0 and CSub2 > 0:
        pass
    elif SSub2 > 0 and CSub2 < 0:
        azimuthSub2 += np.pi
    elif SSub2 < 0 and CSub2 > 0:
        azimuthSub2 += 2 * np.pi
    elif SSub2 < 0 and CSub2 < 0:
        azimuthSub2 += np.pi
    result = (RSub2 * np.cos(azimuthSub2 - 2 * np.arctan(sin_/float(cos_))) - np.power(R,4))\
                /float(np.power(1-R,2))
    return result


def raotest(azimuths, alpha=0.01):
    tableraoII = np.array([247.32, 231.22, 221.14, 186.45, 168.02,
                            111.72, 61.48, 245.19, 232.98, 211.93, 183.44, 168.66,
                            116.3, 69.98, 236.81, 216.05, 206.79, 180.65, 166.3,
                            118.95, 76.52, 229.46, 211.57, 202.55, 177.83, 165.05,
                            121.13, 81.43, 224.41, 206.91, 198.46, 175.68, 163.56,
                            122.57, 85.23, 219.52, 203.17, 195.27, 173.68, 162.36,
                            123.74, 88.35, 215.44, 199.91, 192.37, 171.98, 161.23,
                            124.64, 90.95, 211.87, 197.04, 189.88, 170.45, 160.24,
                            125.38, 93.15, 208.69, 194.51, 187.66, 169.09, 159.33,
                            125.99, 95.05, 205.87, 192.25, 185.68, 167.87, 158.5,
                            126.5, 96.71, 203.33, 190.23, 183.9, 166.76, 157.75,
                            126.94, 98.17, 201.04, 188.39, 182.28, 165.75, 157.06,
                            127.32, 99.47, 198.96, 186.72, 180.81, 164.83, 156.43,
                            127.64, 100.64, 197.05, 185.19, 179.46, 163.98, 155.84,
                            127.93, 101.7, 195.29, 183.78, 178.22, 163.2, 155.29,
                            128.19, 102.67, 193.67, 182.48, 177.08, 162.47, 154.78,
                            128.42, 103.55, 192.17, 181.27, 176.01, 161.79, 154.31,
                            128.62, 104.36, 190.78, 180.15, 175.02, 161.16, 153.86,
                            128.81, 105.1, 189.47, 179.1, 174.1, 160.56, 153.44,
                            128.98, 105.8, 188.25, 178.11, 173.23, 160.01, 153.05,
                            129.13, 106.44, 187.11, 177.19, 172.41, 159.48, 152.68,
                            129.27, 107.04, 186.03, 176.32, 171.64, 158.99, 152.32,
                            129.4, 107.61, 185.01, 175.5, 170.92, 158.52, 151.99,
                            129.52, 108.13, 184.05, 174.73, 170.23, 158.07, 151.67,
                            129.63, 108.63, 183.14, 173.99, 169.58, 157.65, 151.37,
                            129.73, 109.1, 182.28, 173.29, 168.96, 157.25, 151.08,
                            129.82, 109.54, 181.45, 172.63, 168.38, 156.87, 150.8,
                            129.91, 109.96, 177.88, 169.74, 165.81, 155.19, 149.59,
                            130.28, 111.76, 174.99, 167.39, 163.73, 153.82, 148.6,
                            130.55, 113.2, 172.58, 165.44, 162, 152.68, 147.76, 130.76,
                            114.38, 170.54, 163.79, 160.53, 151.7, 147.05, 130.93,
                            115.37, 163.6, 158.13, 155.49, 148.34, 144.56, 131.44,
                            118.68, 159.45, 154.74, 152.46, 146.29, 143.03, 131.69,
                            120.62, 154.51, 150.69, 148.84, 143.83, 141.18, 131.94,
                            122.88, 151.56, 148.26, 146.67, 142.35, 140.06, 132.06,
                            124.21, 148.06, 145.38, 144.09, 140.57, 138.71, 132.19,
                            125.76, 145.96, 143.66, 142.54, 139.5, 137.89, 132.25,
                            126.68, 144.54, 142.48, 141.48, 138.77, 137.33, 132.29,
                            127.3, 143.48, 141.6, 140.7, 138.23, 136.91, 132.31,
                            127.76, 142.66, 140.93, 140.09, 137.8, 136.59, 132.33,
                            128.11, 142, 140.38, 139.6, 137.46, 136.33, 132.34, 128.4,
                            141.45, 139.93, 139.19, 137.18, 136.11, 132.35, 128.63,
                            140.99, 139.54, 138.84, 136.94, 135.92, 132.36, 128.83])
    tableraoII = tableraoII.reshape(43,7)
    v = np.sort(azimuths)
    n = azimuths.shape[0]
    # Ti = [ np.diff(v) , 360 - (v[n-1] - v[0]) ]
    Ti = np.diff(v)
    Ti = np.append(Ti, 360 - (v[n-1] - v[0]))
    L  = (1/float(2)) * np.sum(abs(Ti - 360/float(n)))
    if n > 4:
        if n <= 30:    trow = n - 3
        elif n <= 32:  trow = 27
        elif n <= 37:  trow = 28
        elif n <= 42:  trow = 29
        elif n <= 47:  trow = 30
        elif n <= 62:  trow = 31
        elif n <= 87:  trow = 32
        elif n <= 125: trow = 33
        elif n <= 175: trow = 34
        elif n <= 250: trow = 35
        elif n <= 350: trow = 36
        elif n <= 450: trow = 37
        elif n <= 550: trow = 38
        elif n <= 650: trow = 39
        elif n <= 750: trow = 40
        elif n <= 850: trow = 41
        elif n <= 850: trow = 42
        else:          trow = 43

        alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 0.9]
        if alpha not in alphas:
            string = "  Alphas value are restricted to \n 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 0.9"
        else:
            value = tableraoII[trow-1, alphas.index(alpha)]
            if value >= L: string = "  Rao Test. the hypothesis of uniformity \n  is accepted for P = " + str(alpha)
            else: string = "  Rao Test: the hypothesis of uniformity \n  is rejected for P = " + str(alpha)
    else:
        string = "  Rao Test: Size of sample incorrect"
    return string + "\n \n"


def rayleightest(azimuths):
    n = azimuths.shape[0]
    m_module = meanmodule(azimuths)
    z = n * np.power(m_module,2)
    p = np.exp(-z)
    if round(p, 3) == 0: string = "  Rayleigh Test: P-value for the \n  hypothesis of uniformity < 0.001"
    else: string = "  Rayleigh Test: P-value for the \n  hypothesis of uniformity = " + str(round(p, 3))
    return string + "\n \n"



def allmodulestatistics(modules, ndig = 2):
    n_elements   = modules.shape[0]
    max_value    = np.max(modules)
    min_value    = np.min(modules)
    range_value  = np.fabs(max_value - min_value)
    m_arithmetic = np.average(modules)
    s_error      = sp_stats.stats.sem(modules)
    s_d_module   = np.std(modules,ddof=1)
    s_d_module_p = np.std(modules)
    v_module     = np.var(modules,ddof=1)
    v_module_p   = np.var(modules)
    cs           = sp_stats.stats.skew(modules, bias=False)
    ca           = sp_stats.stats.kurtosis(modules,bias=False)
    formatSpec = '.'+str(ndig)+'f'
    string  = ("  LINEAR STATISTICS - MODULES  "+ "\n")
    string += ("  ---------------------------  "+ "\n")
    string += ("  NUMBER OF ELEMENTS = " +str(n_elements)+ "\n")
    string += ("  MIN VALUE = "                     + str(format(round(min_value,    ndig),formatSpec))+ "\n")
    string += ("  MAX VALUE = "                     + str(format(round(max_value,    ndig),formatSpec))+ "\n")
    string += ("  RANGE = "                         + str(format(round(range_value,  ndig),formatSpec))+ "\n")
    string += ("  ARITHMETIC MEAN = "               + str(format(round(m_arithmetic, ndig),formatSpec))+ "\n")
    string += ("  MEAN STANDARD ERROR = "           + str(format(round(s_error,      ndig),formatSpec))+ "\n")
    string += ("  STANDARD DEVIATION = "            + str(format(round(s_d_module,   ndig),formatSpec))+ "\n")
    string += ("  VARIANCE = "                      + str(format(round(v_module,     ndig),formatSpec))+ "\n")
    string += ("  POPULATION STANDARD DEVIATION = " + str(format(round(s_d_module_p, ndig),formatSpec))+ "\n")
    string += ("  POPULATION VARIANCE = "           + str(format(round(v_module_p,   ndig),formatSpec))+ "\n")
    string += ("  SKEWNESS COEFFICIENT = "          + str(format(round(cs,           ndig),formatSpec))+ "\n")
    string += ("  KURTOSIS COEFFICIENT = "          + str(format(round(ca,           ndig),formatSpec)) + "\n")
    return string + "\n"


def allazimuthstatistic(azimuths, ndig=2):
    n_elements   = azimuths.shape[0]
    m_azimuth    = averageazimuth(azimuths)
    m_module     = meanmodule(azimuths)
    c_variance   = circularvariance(azimuths)
    s_deviation  = circularstandarddeviation(azimuths)
    c_dispersal  = circulardispersal(azimuths)
    vm_parameter = vonmisesparameter(azimuths)
    s_azimuth    = skewnessazimuthcoefficient(azimuths)
    k_azimuth    = kurtosisazimuthcoefficient(azimuths)

    formatSpec = '.'+str(ndig)+'f'
    string  = "  ------------------------------  " + "\n"
    string += ("  CIRCULAR STATISTICS - AZIMUTHS  " + "\n")
    string += ("  ------------------------------  " + "\n")
    string += ("  NUMBER OF ELEMENTS = " +str(n_elements) + "\n")
    string += ("  MEAN AZIMUTH = "    + str(format(round(m_azimuth,    ndig),formatSpec)) + "\n")
    string += ("  MEAN MODULE = "    + str(format(round(m_module,    ndig),formatSpec)) + "\n")
    string += ("  CIRCULAR STANDARD DEVIATION = "    + str(format(round(s_deviation,    ndig),formatSpec)) + "\n")
    string += ("  CIRCULAR VARIANCE = "    + str(format(round(c_variance,    ndig),formatSpec)) + "\n")
    string += ("  CIRCULAR DISPERSAL = "    + str(format(round(c_dispersal,    ndig),formatSpec)) + "\n")
    string += ("  VON MISES PARAMETER = "    + str(format(round(vm_parameter,    ndig),formatSpec)) + "\n")
    string += ("  SKEWNESS COEFFICIENT = "    + str(format(round(s_azimuth,    ndig),formatSpec)) + "\n")
    string += ("  KURTOSIS COEFFICIENT = "    + str(format(round(k_azimuth,    ndig),formatSpec)) + "\n")
    return string + "\n"

def allharmonicMean(vectors):
    n = vectors.shape[0]
    m = np.zeros(n).reshape(n,1)
    for i in range(n):
        num1   = (vectors[i,1]-vectors[i,0])**2
        numpy1 = (np.delete(vectors[:,1],i) - np.delete(vectors[:,0],i)) **2
        m[i]= n//float(np.sum(1/np.sqrt(np.add(num1,numpy1))))
    return m


def kde2D(x, y, bandwidth, xbins=200j, ybins=200j, **kwargs): 
    """Build 2D kernel density estimate (KDE)."""

    # create grid of sample locations (default: 200x200)
    xx, yy = np.mgrid[x.min()*1.1:x.max()*1.1:xbins, 
                        y.min()*1.1:y.max()*1.1:ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T

    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
    kde_skl.fit(xy_train)

    # score_samples() returns the log-likelihood of the samples
    z = np.exp(kde_skl.score_samples(xy_sample))
    return xx, yy, np.reshape(z, xx.shape)
