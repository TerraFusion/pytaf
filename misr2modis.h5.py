"""
This is a demo program that plots misr2modis.h5.
The misr2modis.h5 is created by misr2modis.py.

Usage:  save this script and run

    $python misr2modis.h5.py

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-11
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

# Open the file.
file_name = 'misr2modis.h5'

with h5py.File(file_name, 'r') as f:
    # Read MISR Radiance dataset.
    # Change dataset name to try either source or target.
    # misr_dset = f['/Source/Data_Fields/MISR_Radiance']
    misr_dset = f['/Target/Data_Fields/MISR_Radiance']        
    misr_data = misr_dset[:].astype(np.float64)
    ds_lat = f['/Geolocation/Latitude']
    lat = ds_lat[:].astype(np.float64)
    ds_lon = f['/Geolocation/Longitude']
    lon = ds_lon[:].astype(np.float64)
# Plot data.
data = misr_data
data[data == -999] = np.nan
datam = np.ma.masked_array(data, np.isnan(data))
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=np.min(lat), urcrnrlat=np.max(lat),
            llcrnrlon=np.min(lon), urcrnrlon=np.max(lon))
slat = (np.ceil(np.max(lat)) -  np.floor(np.min(lat))) / 6.0
slon = (np.ceil(np.max(lon)) -  np.floor(np.min(lon))) / 6.0        
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(np.floor(np.min(lat)),
                          np.ceil(np.max(lat)), slat),
                labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(np.floor(np.min(lon)),
                          np.ceil(np.max(lon)), slon),
                labels=[0, 0, 0, 1])
# m.pcolormesh(lon, lat, datam, latlon=True, cmap='jet')
m.scatter(lon, lat, c=datam, s=1, edgecolors=None, linewidth=0)
fig = plt.gcf()
fig.suptitle('{0}'.format(file_name))
# Change output file name depending on source or target.
# pngfile = file_name+'.py.s.png'
pngfile = file_name+'.py.t.png'
fig.savefig(pngfile)
