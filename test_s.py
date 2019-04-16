import pytaf
import numpy as np

print('Testing summary interpolation.')
slat = np.arange(12, dtype=np.float64).reshape((3,4))
slon = np.arange(12, dtype=np.float64).reshape((3,4))
c = np.arange(3, dtype=np.int32)
tlat = np.arange(12, dtype=np.float64).reshape((3,4))
tlon = np.arange(12, dtype=np.float64).reshape((3,4))
sdata = slat * -333
# radius
r = 5555

tsd = np.arange(12, dtype=np.float64).reshape((3,4))
print(tsd)
npix = np.arange(12, dtype=np.int32).reshape((3,4))
print(npix)
j = pytaf.resample_s(slat, slon, tlat, tlon, sdata, r, tsd, npix)
print(j)
print(tsd)
print(npix)
print('Finished testing summary interpolation.')
