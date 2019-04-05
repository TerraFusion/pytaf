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


print('Test nearest neighbor resample.')
g = pytaf.resample_n(a, b, d, e, f, r)
print(g)

print('Test summary resample.')
g1 = pytaf.resample_s(a, b, d, e, f, r)
print(g1)


# Test dimension size error.
print('Test dimension size error')
h = np.arange(12, dtype=np.float64).reshape((3,2,2))

# Test 3D var for source lat.
i = pytaf.resample_n(h, b, d, e, f, r)

# Test 3D var for source var.
j = pytaf.resample_s(a, b, d, e, h, r)

# Test 1D lat/lon in target. Useful for geo-graphic projection.
k = np.arange(3)
l = np.arange(4)

# Test 1D var for target lat and 2D var for target lon.
print('Test dimension mismatch.')
m0 = pytaf.resample_n(a, b, k, e, f, r)

# Test 1D lat/lon.
print('Test 1D lat/lon nn.')
# m = pytaf.resample_n(a, b, k, l, f, r)
# print(m)
print('Test 1D lat/lon summary.')
# n = pytaf.resample_s(a, b, k, l, f, r)
# print(n)
