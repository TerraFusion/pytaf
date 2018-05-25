import h5py
import pytaf
import numpy as np

# Open BF file.
file_name = '/Users/hyoklee/Downloads/TERRA_BF_L1B_O69626_20130119123228_F000_V000.h5'
with h5py.File(file_name, 'r') as f:
    # Read MISR / AN / Blue_Radiance dataset.
    misr_dset = f['/MISR/AN/Data_Fields/Blue_Radiance']
    misr_data = misr_dset[0,:,:].astype(np.float64)

    # How does AF collect all MODIS dataset and merge?
    # TODO: Do something like get_modis_rads() in io.cpp.
    
    # Read MODIS 1km band 8 dataset.
    modis_dset = f['/MODIS/granule_2013019_1310/_1KM/Data_Fields/EV_1KM_RefSB']
    modis_data = modis_dset[0,:,:].astype(np.float64)

c = np.arange(3, dtype=np.int32)
print(modis_data[0,0:10])
print(misr_data[0,0:10])

# TODO: On what dataset interpolate should be called?
# Do some processing in io.cpp and AF_output_MODIS/MISR.cpp.
pytaf.interpolate_nn(modis_data, misr_data, c, 3)
print(misr_data[0,0:10])

# Open file for writing.
f2 = h5py.File('misr_on_modis.h5', 'w')
dset = f2.create_dataset('/Target/Data_Fields/MISR_Radiance', data=misr_data)
dset2 = f2.create_dataset('/Source/Data_Fields/MODIS_Radiance', data=modis_data)
f2.close()
