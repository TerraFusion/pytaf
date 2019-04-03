import h5py
import pytaf
import numpy as np
import gdal

# Open AF file.
file_name = '/Users/hyoklee/Downloads/misr_on_modis_SrcLowAnAfBlueGreen_Trg1KM8_9_69365.h5'

# Generate lat/lon from GDAL.
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
cellSize = 0.05
x0, xinc, y0, yinc = (-180, cellSize, 90, -cellSize)
nx, ny = (360*20, 180*20)
# nx, ny = (360, 180)
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)
lon, lat = np.meshgrid(x, y)
print(lon[0,0])
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

# Set max radius.
M_PI=3.14159265358979323846
earthRadius = 6367444
max_r = earthRadius * cellSize * M_PI / 180

index = np.arange(nx*ny, dtype=np.int32)
distance = np.arange(nx*ny, dtype=np.float64).reshape((nx,ny))

# Kent: try nnInterploate first.
# In the summaryInterpolate, tarSD and nSouPixels are also output parameters.
n_src = modis_lat.size;
print(n_src)
n_trg = nx * ny;
print(n_trg)

# Find indexes of nearest neighbor point.
pytaf.find_nn_block_index(modis_lat, modis_lon,
                          n_src,
                          lat, lon,
                          index, distance,
                          n_trg,
                          max_r)
print('Finished generating index.')
# Get values for target.
trg_data = np.arange(nx*ny, dtype=np.float64).reshape((nx,ny))
pytaf.interpolate_nn(modis_data, trg_data, index, n_trg)
print(trg_data)
print('Finished retrieving data with index.')

# Open file for writing.
f2 = h5py.File('modis_on_ug.h5', 'w')
dset = f2.create_dataset('/Target/Data_Fields/UG_Radiance', data=trg_data)
dset2 = f2.create_dataset('/Source/Data_Fields/MODIS_Radiance', data=modis_data)

# TODO: Add CF attributes on dataset.
f2.close()

# TODO: Plot data.

# References
# [1] https://github.com/TerraFusion/advancedFusion/blob/master/src/AFtool.cpp
