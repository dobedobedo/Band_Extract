# -*- coding: utf-8 -*-
"""
Created on Mon May 15 06:58:29 2017

@author: o0331
"""

import os
import numpy as np
import gdal
from osgeo import gdal_array
import tkinter as tk
from tkinter.filedialog import askopenfilename

def Read_Image(Fullfilename):
    path, filename = os.path.split(Fullfilename)
    filename, ext = os.path.splitext(filename)
    
    InputFile = gdal.Open(Fullfilename)
    cols = InputFile.RasterXSize
    rows = InputFile.RasterYSize
    channel = InputFile.RasterCount
    GeoTransform = InputFile.GetGeoTransform()
    Projection = InputFile.GetProjection()
    driver = InputFile.GetDriver()
    bands = []
    for band in range(channel):
        bands.append(InputFile.GetRasterBand(band+1))
    ndv = bands[band].GetNoDataValue()
    image = np.zeros((rows,cols), dtype=InputFile.ReadAsArray().dtype)
    
    for band in range(channel):
        image = bands[band].ReadAsArray(0,0,cols,rows)
        OutFile = os.path.join(path,filename+'_band{}.tif'.format(band+1))
        Type = gdal_array.NumericTypeCodeToGDALTypeCode(image.dtype.type)
        OutImage = driver.Create(OutFile, 
                                     image.shape[1], image.shape[0], 1, Type)
        OutImage.GetRasterBand(1).WriteArray(image[:,:])
        if ndv is not None:
            OutImage.GetRasterBand(1).SetNoDataValue(ndv)
        OutImage.SetGeoTransform(GeoTransform)
        OutImage.SetProjection(Projection)
        OutImage = None

    InputFile = None    

gdal.AllRegister()
tk.Tk().withdraw()
Fullfilename=askopenfilename(filetypes=[("Tiff","*.tif;*.TIF;*tiff;*TIFF")])
Read_Image(Fullfilename)
