import numpy as np
import h5py
import pytaf
import time

start_time = time.time()
bf_file = 'TERRA_BF_L1B_O53557_20100112014327_F000_V001.h5'
max_radius = 20000

# ---- CERES part -----
lat = np.array([])
lon = np.array([])
sza = np.array([])
vza = np.array([])

with h5py.File(bf_file) as h5f:
    for i in h5f['CERES']:
        lat = np.append(lat, h5f['CERES/{}/FM1/Time_and_Position/Latitude'.format(i)][:])
        lon = np.append(lon, h5f['CERES/{}/FM1/Time_and_Position/Longitude'.format(i)][:])
        sza = np.append(sza, h5f['CERES/{}/FM1/Viewing_Angles/Solar_Zenith'.format(i)][:])
        vza = np.append(vza, h5f['CERES/{}/FM1/Viewing_Angles/Viewing_Zenith'.format(i)][:])
        
# Apply criteria.
idx = np.where((sza>=0)&(sza<=89)&(vza>=0)&(vza<=25))[0]
print(idx.shape)
target_lat = lat[idx]
target_lon = lon[idx]


# ---- MISR part ----
with h5py.File(bf_file) as h5f:
    var = h5f['MISR/AN/Data_Fields/Red_Radiance'][:]
    lat = h5f['MISR/HRGeolocation/GeoLatitude'][:]
    lon = h5f['MISR/HRGeolocation/GeoLongitude'][:]

# Convert 3-D MISR grids to 2-D.
src_var = np.vstack(var).astype(np.float64)
print(src_var.shape)
src_lat = np.vstack(lat).astype(np.float64)
src_lon = np.vstack(lon).astype(np.float64)

# Call resample using summary interpolation.
sd = np.zeros(src_var.shape, dtype=src_var.dtype)
npix = np.zeros(src_var.shape, dtype=np.int32)

# Make copies of target lat/lon because resample will modify them.
tlat = target_lat.copy()
tlon = target_lon.copy()
trg_data = pytaf.resample_s(src_lat, src_lon, target_lat, target_lon, 
                            src_var, max_radius, sd, npix)

print(trg_data.shape)
print(trg_data.size)
print(trg_data)

# Write data for plotting.
f3 = h5py.File('misr2ceres.h5', 'w')
dset = f3.create_dataset('/Target/Data_Fields/MISR_AN_Red_Radiance', data=trg_data)
dset3 = f3.create_dataset('/Geolocation/Latitude', data=tlat)
dset4 = f3.create_dataset('/Geolocation/Longitude', data=tlon)
f3.close()

print("--- %s seconds ---" % (time.time() - start_time))
