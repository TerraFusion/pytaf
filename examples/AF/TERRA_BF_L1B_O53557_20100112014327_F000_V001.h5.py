"""
This is a demo program that plots CERES dataset from BF file.

Usage:  save this script and run

    $python TERRA_BF_L1B_O53557_20100112014327_F000_V001.h5.py

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-16

"""
import time
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# If you encounter PROJ_LIB key error on Python3,
# please run:
#
# $export PROJ_LIB=~/anaconda3/share/proj/

start_time = time.time()

# Open the file.
file_name = 'TERRA_BF_L1B_O53557_20100112014327_F000_V001.h5'

lat = np.array([])
lon = np.array([])
sza = np.array([])
vza = np.array([])

with h5py.File(file_name) as h5f:
    for i in h5f['CERES']:
        lat = np.append(lat, h5f['CERES/{}/FM1/Time_and_Position/Latitude'.format(i)][:])
        lon = np.append(lon, h5f['CERES/{}/FM1/Time_and_Position/Longitude'.format(i)][:])
        sza = np.append(sza, h5f['CERES/{}/FM1/Viewing_Angles/Solar_Zenith'.format(i)][:])
        vza = np.append(vza, h5f['CERES/{}/FM1/Viewing_Angles/Viewing_Zenith'.format(i)][:])
        
# Apply criteria.
idx = np.where((sza>=0)&(sza<=89)&(vza>=0)&(vza<=25))[0]
target_lat = lat[idx]
target_lon = lon[idx]
target_sza = sza[idx]

# Plot data.
data = target_sza
data[data == -999] = np.nan
datam = np.ma.masked_array(data, np.isnan(data))
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=np.min(target_lat), urcrnrlat=np.max(target_lat),
            llcrnrlon=np.min(target_lon), urcrnrlon=np.max(target_lon))
slat = (np.ceil(np.max(lat)) -  np.floor(np.min(lat))) / 6.0
slon = (np.ceil(np.max(lon)) -  np.floor(np.min(lon))) / 6.0        
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(np.floor(np.min(lat)),
                          np.ceil(np.max(lat)), slat),
                labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(np.floor(np.min(lon)),
                          np.ceil(np.max(lon)), slon),
                labels=[0, 0, 0, 1])
m.scatter(target_lon, target_lat, c=datam, s=1, edgecolors=None, linewidth=0)
fig = plt.gcf()
fig.suptitle('{0}'.format(file_name))
pngfile = file_name+'.py.png'
fig.savefig(pngfile)
print("--- %s seconds ---" % (time.time() - start_time))
