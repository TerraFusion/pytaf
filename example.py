import pytaf
import numpy as np
a = np.arange(12, dtype=np.float64).reshape((3,4))
b = a * -333
c = np.arange(3, dtype=np.int32)
print(a)
pytaf.clip(a, b, 4)
print(a)
print(b)
pytaf.interpolate_nn(a, b, c, 3)
print(b)
d = np.arange(12, dtype=np.float64).reshape((3,4))
print(d.shape)
e = np.arange(12, dtype=np.float64).reshape((3,4))
f = np.arange(12, dtype=np.float64).reshape((3,4))
pytaf.find_nn_block_index(d, e, 3, a, b, c, f, 3, 90.0)
print(b)
# radius
r = 5555 
g = pytaf.resample_n(a, b, d, e, f, r)
print(g)
# Test dimension size error.
h = np.arange(12, dtype=np.float64).reshape((3,2,2))
i = pytaf.resample_n(h, b, d, e, f, r)
j = pytaf.resample_s(a, b, d, e, h, r)
