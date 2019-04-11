import pytaf
import numpy as np
slat = np.arange(12, dtype=np.float64)
slon = np.arange(12, dtype=np.float64)
sdata = slat * -333
tlat = np.arange(12, dtype=np.float64).reshape((3,4))
tlon = np.arange(12, dtype=np.float64).reshape((3,4))
# radius
r = 5555


print('Test nearest neighbor resample with 1d src lat/lon/data.')
g = pytaf.resample_n(slat, slon, tlat, tlon, sdata, r)
print(g)
