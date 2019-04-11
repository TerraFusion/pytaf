# Test low level function for summary.
import pytaf
import numpy as np

slat = np.arange(12, dtype=np.float64).reshape((3,4))
slon = np.arange(12, dtype=np.float64).reshape((3,4))
sdata = slat * -333
tlat = np.arange(12, dtype=np.float64).reshape((3,4))
tlon = np.arange(12, dtype=np.float64).reshape((3,4))

# radius
r = 5555

print('Test summary resample with 2 additional arguments.')
distance = np.arange(12, dtype=np.float64).reshape((3,4))
index = np.arange(12, dtype=np.int32)
pytaf.find_nn_block_index(slat, slon, sdata.size, tlat, tlon,
                          index, distance, tlat.size, r)
tdata = np.zeros((3,4), dtype=sdata.dtype)
print(tdata)
tsd = np.zeros((3,4), dtype=sdata.dtype)
nsp = np.arange((3,4), dtype=np.int32)
pytaf.interpolate_summary(sdata, index, sdata.size,
                          tdata, tsd, nsp, tdata.size)
print(tdata)
