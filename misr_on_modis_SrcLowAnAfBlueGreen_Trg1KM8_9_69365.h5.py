"""
This example code illustrates how to access and visualize a TerraFusion
Advanced Fusion file in Python.

Usage:  save this script and run

    $python misr_on_modis_SrcLowAnAfBlueGreen_Trg1KM8_9_69365.h5.py

The HDF file must be in your current working directory.

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-03
"""
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# If you encounter PROJ_LIB key error on Python3,
# please run:
#
# $export PROJ_LIB=~/anaconda3/share/proj/

# Open AF file.
file_name = 'misr_on_modis_SrcLowAnAfBlueGreen_Trg1KM8_9_69365.h5'

with h5py.File(file_name, 'r') as f:
    # Read MODIS Radiance dataset.
    modis_dset = f['/Target/Data_Fields/MODIS_Radiance']
    modis_data = modis_dset[0,:,:].astype(np.float64)
    # print(modis_data[0,0:10])
    # Read source lat/lon dataset.
    modis_ds_lat = f['/Geolocation/Latitude']
    modis_lat = modis_ds_lat[:,:].astype(np.float64)

    modis_ds_lon = f['/Geolocation/Longitude']
    modis_lon = modis_ds_lon[:,:].astype(np.float64)
# Plot data.
data = modis_data
data[data == -999] = np.nan
datam = np.ma.masked_array(data, np.isnan(data))
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=-90, urcrnrlat = 90,
            llcrnrlon=-180, urcrnrlon = 180)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180, 180., 45.), labels=[0, 0, 0, 1])
# Render the image in the projected coordinate system.
# s = 1000
# m.pcolormesh(modis_lon[::s,::s], modis_lat[::s,::s], modis_data[::s,::s],
#              latlon=True)
m.scatter(modis_lon, modis_lat, c=datam, s=1,
          edgecolors=None, linewidth=0)
fig = plt.gcf()
pngfile = file_name+'.py.png'
fig.savefig(pngfile)
