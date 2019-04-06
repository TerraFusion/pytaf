"""
This example code illustrates how to access and reproject a TerraFusion
Advanced Fusion file in Python.

Usage:  save this script and run

    $python modis2ug.rn.py

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
cellSize = 0.05
x0, xinc, y0, yinc = (-180, cellSize, 90, -cellSize)
nx, ny = (360*20, 180*20)
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)

with h5py.File(file_name, 'r') as f:
    # Read MODIS Radiance dataset.
    modis_dset = f['/Target/Data_Fields/MODIS_Radiance']
    modis_data = modis_dset[0,:,:].astype(np.float64)
    print(modis_data[0,0:10])
    # Read source lat/lon dataset.
    modis_ds_lat = f['/Geolocation/Latitude']
    modis_lat = modis_ds_lat[:,:].astype(np.float64)
    modis_ds_lon = f['/Geolocation/Longitude']
    modis_lon = modis_ds_lon[:,:].astype(np.float64)
f.close()

# Set max radius.
M_PI=3.14159265358979323846
earthRadius = 6367444
max_r = earthRadius * cellSize * M_PI / 180

index = np.arange(nx*ny, dtype=np.int32)
distance = np.arange(nx*ny, dtype=np.float64).reshape((ny,nx))

# Kent: try nnInterploate first.
# In the summaryInterpolate, tarSD and nSouPixels are also output parameters.
n_src = modis_lat.size;
print(n_src)
n_trg = nx * ny;
print(n_trg)

# Find indexes of nearest neighbor point.
trg_data = pytaf.resample_n(modis_lat, modis_lon, 
                            x, y, modis_data, max_r)
print(trg_data)
print('Finished retrieving data with index.')

# Open file for writing.
f2 = h5py.File('modis2ug.rn.h5', 'w')
dset = f2.create_dataset('/UG_Radiance', data=trg_data)
dset_lat = f2.create_dataset('/Latitude', data=y)
dset_lon = f2.create_dataset('/Longitude', data=x)

# TODO: Add CF attributes on dataset.
f2.close()

