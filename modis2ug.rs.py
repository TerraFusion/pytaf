"""
This example code illustrates how to access and reproject a TerraFusion
Advanced Fusion file in Python.

Usage:  save this script and run

    $python modis2ug.rs.py

The HDF file must be in your current working directory.

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-05
"""
import h5py
import pytaf
import numpy as np
import gdal

# Open AF file.
file_name = 'misr_on_modis_SrcLowAnAfBlueGreen_Trg1KM8_9_69365.h5'

# Generate 1-d lat/lon.
cellSize = 1
x0, xinc, y0, yinc = (-180, cellSize, 90, -cellSize)
nx, ny = (360, 180)
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)

with h5py.File(file_name, 'r') as f:
    # Read MODIS Radiance dataset.
    modis_dset = f['/Target/Data_Fields/MODIS_Radiance']
    modis_data = modis_dset[0,:,:].astype(np.float64)
    # Read source lat/lon dataset.
    modis_ds_lat = f['/Geolocation/Latitude']
    modis_lat = modis_ds_lat[:,:].astype(np.float64)
    modis_ds_lon = f['/Geolocation/Longitude']
    modis_lon = modis_ds_lon[:,:].astype(np.float64)
f.close()

max_r = 5040

# Find indexes of nearest neighbor point.


lon, lat = np.meshgrid(x, y)
latd = np.array(lat, dtype='float64')
lond = np.array(lon, dtype='float64')
lat_orig = latd.copy()
lon_orig = lond.copy()

# Create dataset for index and distance.
n_src = modis_lat.size;
sx = modis_lat.shape[0]
sy = modis_lat.shape[1]
index = np.arange(n_src, dtype=np.int32)
distance = np.arange(n_src, dtype=np.float64).reshape((sy,sx))

# For some reason, passing 1-d generates memory error.
# trg_data = pytaf.resample_s(modis_lat, modis_lon, 
#                             y, x, modis_data, max_r, distance, index)
trg_data = pytaf.resample(modis_lat, modis_lon,
                          latd, lond,
                          modis_data, max_r, True, distance, index)
print('resample_s is done')
print(trg_data)

# Open file for writing.
f2 = h5py.File('modis2ug.rs.h5', 'w')
dset = f2.create_dataset('/UG_Radiance', data=trg_data)
dset_lat = f2.create_dataset('/Latitude', data=y)
dset_lon = f2.create_dataset('/Longitude', data=x)
# dset_lat = f2.create_dataset('/Latitude', data=lat_orig)
# dset_lon = f2.create_dataset('/Longitude', data=lon_orig)

# TODO: Add CF attributes on dataset.
f2.close()

