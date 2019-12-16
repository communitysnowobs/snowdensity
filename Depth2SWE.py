#!/usr/bin/env python
# coding: utf-8

#################### SWE Calculator ####################
# This script implements a power law regression in order to produce a value of snow water equivalent (SWE) based on various parameters associated with a snow depth measurement. The input variables can be scalars (single measurement) or vectors (batch measurements). The following information on units, etc., is critical. To use this script, edit inputs with your data.

# Christina Aragon, Oregon State University 
# December 2019
#######################################################################

#################### Data ####################

# Gridded winter precipitation (PPTWT) and temperature difference (TD) data is used in this script. See https://adaptwest.databasin.org/pages/adaptwest-climatena for info on data. See http://www.cacpd.org.s3-website-us-west-2.amazonaws.com/climate_normals/NA_ReadMe.txt for specific metadata.
# The grids that are included with this calculator have been put into geographic coords and they have been clipped to (72>lat>30) and (-168<lon<-60).
# 
##################### User Defined Inputs ####################
# 
# #### H: snow depth [mm]
# #### Y: year
# #### M: month [1 to 12]
# #### D: day [1 to 31] 
# #### LAT: latitude [degrees]
# Positive for N. Hemisphere
# #### LON: longitude [degrees]
# Signed - ex: -120 for N America 
# 
#################### Outputs ####################
# 
# #### SWE: snow water equivalent [mm]
# #### DOY: day of water year [Oct 1 = 1]

########################################################################
import numpy as np
from osgeo import gdal
from scipy.interpolate import interp2d
from datetime import date

#***Edit input data***. Input variables can be a list or array. 
#Below is an example of manually entered inputs, or data can be imported from .txt, .csv, etc. 
Y = [2018,2018,2018]
M = [1,11,3]
D = [1,1,1]
H = [30,40,50]
LAT = [43.5,43.5,43.5]
LON = [-110.8,-110.8,-110.8]

#Build lat/lon array 
ncols = 7300
nrows = 2839
xll = -168.00051894775
yll = 30.002598288104
clsz = 0.014795907586
#Longitudes
ln = np.arange(xll, xll+ncols*clsz, clsz)
#Latitudes
lt = np.arange(yll, yll+nrows*clsz, clsz)
la = np.flipud(lt)

#Import temperature difference data
geo = gdal.Open('td_final.txt')
td = geo.ReadAsArray()
#Import winter precipitation data
geo = gdal.Open('ppt_wt_final.txt')
pptwt = geo.ReadAsArray()
    
def swe_calc(Y,M,D,H,LAT,LON):
    #Interpolate temp to input
    f_td = interp2d(ln, la, td, kind='cubic')
    TD = f_td(LON, LAT)
    #Interpolate temp to input
    f_ppt = interp2d(ln, la, pptwt, kind='cubic')
    PPTWT = f_ppt(LON, LAT)
    #Determine day of year
    DOY = date.toordinal(date(Y,M,D))-date.toordinal(date(Y,9,30))
    if DOY < 0:
        DOY = DOY+365
    #Apply regression equation 
    a = [0.0533,0.948,0.1701,-0.1314,0.2922] #accumulation phase
    b = [0.0481,1.0395,0.1699,-0.0461,0.1804]; #ablation phase
    SWE = a[0]*H**a[1]*PPTWT**a[2]*TD**a[3]*DOY**a[4]*     (-np.tanh(.01*(DOY-180))+1)/2 + b[0]*H**b[1]*     PPTWT**b[2]*TD**b[3]*DOY**b[4] * (np.tanh(.01*(DOY-180))+1)/2;
    return SWE,DOY

#Create output arrays 
SWE = np.zeros(len(H))*np.nan
DOY = np.zeros(len(H))*np.nan
for i in np.arange(len(H)):
    swe, doy = swe_calc(Y[i],M[i],D[i],H[i],LAT[i],LON[i])
    SWE[i] = swe
    DOY[i] = doy

#Optional: print output SWE and DOY 
#print(SWE)
#print(DOY)
