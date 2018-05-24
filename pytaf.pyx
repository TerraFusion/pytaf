"""
taf.pyx

simple cython test of accessing a numpy array's data

the C function: c_multiply multiplies all the values in a 2-d array by a scalar, in place.

"""

import cython

# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as np

# declare the interface to the C code
# cdef extern void c_multiply (double* array, double value, int m, int n)
cdef extern void clipping(double * val, double * mask, int nPixels)
@cython.boundscheck(False)
@cython.wraparound(False)
def clip(np.ndarray[double, ndim=2, mode="c"] val not None,
             np.ndarray[double, ndim=2, mode="c"] mask not None,
             int nPixels):
    """
    clip(val, mask,  value)

    param: val -- a 2-d numpy array of np.float64
    param: mask -- a 2-d numpy array of np.float64
    param: nPixesl -- an integer

    """
    clipping(&val[0,0], &mask[0,0], nPixels)
    return None

