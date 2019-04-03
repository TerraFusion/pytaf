import h5py
import pytaf
import numpy as np
import gdal

# Open AF file.
file_name = '/Users/hyoklee/Downloads/misr_on_modis_SrcLowAnAfBlueGreen_Trg1KM8_9_69365.h5'

# TODO: Generate lat/lon from GDAL.
#
# This correspodns to AFtool.c:
#
# AF_GetGeolocationDataFromInstrument(std::string instrument, AF_InputParmeterFile &inputArgs, hid_t inputFile, double **latitude /*OUT*/, double **longitude /*OUT*/, int &cellNum /*OUT*/)

# USER_OUTPUT_EPSG: 4326
# USER_X_MIN: -180
# USER_X_MAX: 180
# USER_Y_MIN: -90
# USER_Y_MAX: 90
# USER_RESOLUTION: 1
    
# Notice if the USER_RESOLUTION is 0.1,1, summaryInterpolate should be used.
# If USER_RESOLUTION is 0.05, or 0.01, nnInterpolate can be used.

# Borrowed from http://hdfeos.org/zoo comprehensive example.
x0, xinc, y0, yinc = (-180, 0.05, 90, -0.05)
nx, ny = (360*20, 180*20)
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)
lon, lat = np.meshgrid(x, y)

with h5py.File(file_name, 'r') as f:
    

    # Read MODIS Radiance dataset.
    modis_dset = f['/Target/Data_Fields/MODIS_Radiance']
    modis_data = modis_dset[0,:,:].astype(np.float64)

    # Read lat/lon dataset.
    modis_ds_lat = f['/Geolocation/Latitude']
    modis_lat = modis_ds_lat[:,:].astype(np.float64)

    modis_ds_lon = f['/Geolocation/Longitude']
    modis_lon = modis_ds_lon[:,:].astype(np.float64)

# Set cell size.
cellSize = 3
M_PI=3.14159265358979323846
earthRadius = 6367444
max_r = earthRadius * cellSize * M_PI / 180

c = np.arange(3, dtype=np.int32)
print(modis_data[0,0:10])
# print(misr_data[0,0:10])

# TODO: On what dataset interpolate should be called?
# Do some processing in io.cpp, af_run.cpp, and AF_output_MODIS/MISR.cpp.

#  Kent: try nnInterploate first. In the summaryInterpolate, tarSD and nSouPixels are also output parameters.
c = np.arange(cellSize, dtype=np.int32)
i = np.arange(nx*ny, dtype=np.float64).reshape((nx,ny))
pytaf.find_nn(modis_lat, modis_lon, cellSize, lat, lon, c, i, cellSize, max_r)
# print(misr_data[0,0:10])

# Open file for writing.
f2 = h5py.File('modis_on_ug.h5', 'w')
dset = f2.create_dataset('/Target/Data_Fields/MISR_Radiance', data=i)
dset2 = f2.create_dataset('/Source/Data_Fields/MODIS_Radiance', data=modis_data)

# TODO: Add CF attributes on dataset.
f2.close()

# Plot data.

# References
# [1] https://github.com/TerraFusion/advancedFusion/blob/master/src/AFtool.cpp
