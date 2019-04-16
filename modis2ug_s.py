"""
This example code illustrates how to access and reproject a TerraFusion 
Advanced Fusion file in Python.

Usage:  save this script and run

    $python modis2ug_s.py

The HDF file must be in your current working directory.

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-03
"""
import h5py
import pytaf
import numpy as np

# Open AF file.
file_name = 'misr_on_modis_SrcLowAnAfBlueGreen_Trg1KM8_9_69365.h5'

# Generate lat/lon manually or from GDAL.
#
# This correspodns to the following function in AFtool.cpp [1]:
#
# AF_GetGeolocationDataFromInstrument(std::string instrument, AF_InputParmeterFile &inputArgs, hid_t inputFile, double **latitude /*OUT*/, double **longitude /*OUT*/, int &cellNum /*OUT*/)
#
# USER_OUTPUT_EPSG: 4326
# USER_X_MIN: -180
# USER_X_MAX: 180
# USER_Y_MIN: -90
# USER_Y_MAX: 90
# USER_RESOLUTION: 1
#    
# Notice if the USER_RESOLUTION is 0.1 or 1, summaryInterpolate should be used.
# If USER_RESOLUTION is 0.05 or 0.01, nnInterpolate can be used.

# Borrowed from http://hdfeos.org/zoo comprehensive example.
cellSize = 1
x0, xinc, y0, yinc = (-180, cellSize, 90, -cellSize)
nx, ny = (360, 180)
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)
lon, lat = np.meshgrid(x, y)
print(lon[ny-1,nx-1])
print(lat[ny-1,nx-1])

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
size = 5040
max_r = earthRadius * size * M_PI / 180

n_src = modis_lat.size;
sx = modis_lat.shape[0]
sy = modis_lat.shape[1]

i = np.arange(n_src, dtype=np.int32)
d = np.arange(n_src, dtype=np.float64).reshape((sy,sx))

print(n_src)
n_trg = nx * ny;
print(n_trg)

lat_orig = lat.copy()
lon_orig = lon.copy()
pytaf.find_nn_block_index(lat_orig, lon_orig,
                          n_trg,
                          modis_lat, modis_lon,
                          i, d,
                          n_src,
                          size)

# The above function modifies lat and lon values. Bug?
print(lat[ny-1,nx-1])
print(lat_orig[ny-1,nx-1])
print('Finished generating index.')

# Get values for target using summary interpolation.
# In the summaryInterpolate, tarSD and nSouPixels are also output parameters.
trg_data = np.arange(n_trg, dtype=np.float64).reshape((ny,nx))
tarSD = np.arange(n_trg, dtype=np.float64).reshape((ny,nx))
nSouPixels = np.arange(n_trg, dtype=np.int32).reshape((ny,nx))

pytaf.interpolate_summary(modis_data, i, n_src,
                          trg_data, tarSD, nSouPixels, n_trg)
print(trg_data)
print('Finished retrieving data with index.')

# Open file for writing.
f2 = h5py.File('modis2ug_s.h5', 'w')
dset = f2.create_dataset('/UG_Radiance', data=trg_data)
dset_lat = f2.create_dataset('/Latitude', data=lat_orig)
dset_lon = f2.create_dataset('/Longitude', data=lon_orig)

# TODO: Add CF attributes on dataset.
f2.close()

# References
# [1] https://github.com/TerraFusion/advancedFusion/blob/master/src/AFtool.cpp
