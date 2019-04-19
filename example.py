import pytaf
import numpy as np

a = np.arange(12, dtype=np.float64).reshape((3,4))
b = a * -333
c = np.arange(3, dtype=np.int32)
print('a value')
print(a)
print('b value')
print(b)
pytaf.clip(a, b, 4)
print('a value after clipping')
print(a)
print('b value before low-level nearest neighbor function')
print(b)
print('Test low-level nearest neighbor with fake ID and numbers of cell')
pytaf.interpolate_nn(a, b, c, 3)
print('b value after low-level nearest neighbor function')
print(b)
d = np.arange(12, dtype=np.float64).reshape((3,4))
e = np.arange(12, dtype=np.float64).reshape((3,4))
c1 = np.arange(12, dtype=np.int32).reshape((3,4))
c2 =  np.arange(12, dtype=np.int32)
print('Source value(a) before low-level summary interpolation')
print(a)
pytaf.interpolate_summary(a, c2, a.size, d, e, c1, d.size)
print('Source value after low-level summary interpolation')
print(d)
print('Source SD value after low-level summary interpolation')
print(e)
print('Source pixel count value after low-level summary interpolation')
print(c1)
f = np.arange(12, dtype=np.float64).reshape((3,4))
print('Testing block index build')
print('Index ID value before testing')
pytaf.find_nn_block_index(d, e, 3, a, b, c, f, 3, 90.0)
print('Index ID value after testing')
print(c)

# radius
r = 5555

print('Test high-level nearest neighbor resample.')

print('Source value(e) before testing')
g = pytaf.resample_n(a, b, d, e, f, r)
print('Source value after resampling')
print(g)

sd = np.arange(12, dtype=np.float64).reshape((3,4))
pc = np.arange(12, dtype=np.int32).reshape((3,4))

print('Test summary resample.')
print('Source value(f) before testing')
print(f)
g1 = pytaf.resample_s(a, b, d, e, f, r,sd,pc)
print('Source value(f) after testing')
print(g1)
print('Source SD value after  summary interpolation')
print(sd)
print('Source pixel count value after  summary interpolation')
print(pc)

# Test 1D lat/lon in target. 
k = np.arange(12,dtype=np.float64)
l = np.arange(12,dtype=np.float64)

# Test 1D var for target lat and 2D var for target lon.
#print('Test dimension mismatch.')
#m0 = pytaf.resample_n(a, b, k, e, f, r)

# Test 1D lat/lon.
print('Test 1D lat/lon nn.')
print('Source value(f) before testing')
print(f)
m = pytaf.resample_n(a, b, k, l, f, r)
print('Source value(m) after testing')
print(m)
print('Test 1D lat/lon summary.')
print('Source value(f) before testing')
print(f)
n = pytaf.resample_s(a, b, k, l, f, r,sd,pc)
print('Source value(n) after testing')
print(n)
#test 1-D resmaple_g geographic projection later
