import pytaf
import numpy as np
a = np.arange(12, dtype=np.float64).reshape((3,4))
b = a * -333
c = np.arange(3, dtype=np.int32)
d = np.arange(12, dtype=np.float64).reshape((3,4))
e = np.arange(12, dtype=np.float64).reshape((3,4))
f = np.arange(12, dtype=np.float64).reshape((3,4))
# radius
r = 5555

print('Test summary resample.')
g = pytaf.resample_s(a, b, d, e, f, r)
print(g)
