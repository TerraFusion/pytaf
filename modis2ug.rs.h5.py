"""
This example code illustrates how to access and visualize a TerraFusion
Advanced Fusion file in Python.

Usage:  save this script and run

    $python modis2ug.rs.h5.py

The HDF file must be in your current working directory.

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-07
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

# Open UG file.
file_name = 'modis2ug.rs.h5'

with h5py.File(file_name, 'r') as f:
    # Read MODIS Radiance dataset.
    modis_dset = f['/UG_Radiance']
    modis_data = modis_dset[:].astype(np.float64)
    # print(modis_data[0,0:10])
    # Read source lat/lon dataset.
    modis_ds_lat = f['/Latitude']
    modis_lat = modis_ds_lat[:].astype(np.float64)

    modis_ds_lon = f['/Longitude']
    modis_lon = modis_ds_lon[:].astype(np.float64)
    print(modis_lon)
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
# m.pcolormesh(modis_lat, modis_lon,  datam.T , latlon=True, cmap='jet')
m.pcolormesh(modis_lon, modis_lat,  datam , latlon=True, cmap='jet')
# m.scatter(modis_lon, modis_lat, c=datam, s=1,
#           edgecolors=None, linewidth=0)
fig = plt.gcf()
fig.suptitle('{0}'.format(file_name))
pngfile = file_name+'.py.png'
fig.savefig(pngfile)
