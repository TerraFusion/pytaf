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

print('Test high-level nearest neighbor resample(1D lat/lon).')

# radius 150 km
r = 150000.

a= np.array([30,33,36,39],dtype=np.float64)
b= np.array([40,43,46,49],dtype=np.float64)
d= np.array([40,37,34,31],dtype=np.float64)
e= np.array([50,47,44,41],dtype=np.float64)
f=np.array([1,2,3,4],dtype=np.float64)
print('Source value(f) before testing')
#should be [1 2 3 4]
print(f)
g = pytaf.resample_n(a, b, d, e, f, r)
print('Source value after resampling')
#should be [4 3 2 1]
print(g)

print('Test high-level nearest neighbor resample(2D lat/lon).')
a= np.array([30,33,36,39],dtype=np.float64).reshape((2,2))
b= np.array([40,43,46,49],dtype=np.float64).reshape((2,2))
d= np.array([40,37,34,31],dtype=np.float64).reshape((2,2))
e= np.array([50,47,44,41],dtype=np.float64).reshape((2,2))
f=np.array([1,2,3,4],dtype=np.float64).reshape((2,2))
print('Source value(f) before testing')
#should be [1 2] [3 4]
print(f)
g = pytaf.resample_n(a, b, d, e, f, r)
print('Source value after resampling')
#should be [4 3] [2 1]
print(g)

# radius 100 km
r = 100000.

print('Test summary resample(1D lat/lon).')
a1 = np.array([30.5,31.5,32.5,33.5,36.5,37.5,38.5,39.5],dtype=np.float64)
b1 = np.array([40.5,41.5,42.5,43.5,46.5,47.5,48.5,49.5],dtype=np.float64)
d1 = np.array([39,37,33,31],dtype=np.float64)
e1 = np.array([49,47,43,41],dtype=np.float64)
f=np.array([1,3,5,7,9,11,13,15],dtype=np.float64)
sd = np.arange(4, dtype=np.float64)
pc = np.arange(4, dtype=np.int32)

print('Source value(f) before testing')
#should be [1 3 5 7 9 11 13 15]
print(f)

g1 = pytaf.resample_s(a1, b1, d1, e1, f, r,sd,pc)
print('Source value(f) after testing')
#should be [14 10 6 2]
print(g1)
print('Source SD value after summary interpolation')
#should be [1 1 1 1]
print(sd)
print('Source pixel count value after  summary interpolation')
#should be [2 2 2 2]
print(pc)

print('Test summary resample(2D lat/lon).')
a1 = np.array([30.5,31.5,32.5,33.5,36.5,37.5,38.5,39.5],dtype=np.float64).reshape(4,2)
b1 = np.array([40.5,41.5,42.5,43.5,46.5,47.5,48.5,49.5],dtype=np.float64).reshape(4,2)
d1 = np.array([39,37,33,31],dtype=np.float64).reshape(2,2)
e1 = np.array([49,47,43,41],dtype=np.float64).reshape(2,2)
f=np.array([1,3,5,7,9,11,13,15],dtype=np.float64).reshape(4,2)
sd = np.arange(4, dtype=np.float64).reshape(2,2)
pc = np.arange(4, dtype=np.int32).reshape(2,2)
print('Source value(f) before testing')
#should be [ 1 3] [5 7] [9 11] [13 15]
print(f)

g1 = pytaf.resample_s(a1, b1, d1, e1, f, r,sd,pc)
print('Source value(f) after testing')
#should be [14 10] [6 2]
print(g1)
print('Source SD value after summary interpolation')
#should be [1 1] [1 1]
print(sd)
print('Source pixel count value after summary interpolation')
#should be [2 2] [2 2]
print(pc)

