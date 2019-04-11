"""
This is a demo program that pytaf output matches AF tool output
using two data files that are created by AF tool.

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-11
"""
import h5py
import pytaf
import numpy as np

# Open BF file.
file_name = 'modis_on_misr_Src1KMAll_TrgLowAll_63290.h5'
file_name2 = 'misr_on_modis_SrcLowAll_Trg1KMAll_63290.h5'

with h5py.File(file_name, 'r') as f:
    # Read MISR from Target as source.
    misr_dset = f['/Target/Data_Fields/MISR_Radiance']
    misr_data = misr_dset[0,0,:,:].astype(np.float64)

    # Read source lat/lon. Shape: {23040, 2092}
    ds_lat = f['/Geolocation/Latitude']
    slat = ds_lat[:,:].astype(np.float64)
    ds_lon = f['/Geolocation/Longitude']
    slon = ds_lon[:,:].astype(np.float64)    
f.close()

with h5py.File(file_name2, 'r') as f2:
    # Read target lat/lon. {40620, 1354}
    ds_tlat = f2['/Geolocation/Latitude']
    tlat = ds_tlat[:,:].astype(np.float64)
    ds_tlon = f2['/Geolocation/Longitude']
    tlon = ds_tlon[:,:].astype(np.float64)        
    ds_tmisr = f2['/Source/Data_Fields/MISR_Radiance']
    tmisr = ds_tmisr[0,0,:,:].astype(np.float64)
f2.close()
lat_orig = tlat.copy()
lon_orig = tlon.copy()

trg_data = pytaf.resample_n(slat, slon, tlat, tlon, misr_data, 5556)
print(trg_data[0,0:10])

# Open file for writing.
f3 = h5py.File('misr2modis.h5', 'w')
dset = f3.create_dataset('/Target/Data_Fields/MISR_Radiance', data=trg_data)
dset2 = f3.create_dataset('/Source/Data_Fields/MISR_Radiance', data=tmisr)
dset3 = f3.create_dataset('/Geolocation/Latitude', data=lat_orig)
dset4 = f3.create_dataset('/Geolocation/Longitude', data=lon_orig)
f3.close()
