"""
pytaf.pyx

simple cython test of accessing advancedFusion functions

The C functions from advancedFusion:

 * reproject.cpp/clipping 
 * reproject.cpp/nnInterpolate
 ...

"""

import cython
from ctypes import *

# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as np

# declare the interface to the C code
cdef extern void clipping(double * val, double * mask, int nPixels)
cdef extern void nearestNeighbor(double ** psouLat, double ** psouLon, int nSou,
                                 double * tarLat, double * tarLon,
                                 int * tarNNSouID, double * tarNNDis,
                                 int nTar, double maxR)
cdef extern void nearestNeighborBlockIndex(
    double ** psouLat, double ** psouLon, int nSou,
    double * tarLat, double * tarLon, int * tarNNSouID,
    double * tarNNDis, int nTar, double maxR)
cdef extern void nnInterpolate(double * souVal, double * tarVal,
                               int * tarNNSouID, int nTar)
cdef extern void summaryInterpolate(double * souVal, int * souNNTarID, int nSou,
                                    double * tarVal, double * tarSD,
                                    int * nSouPixels, int nTar)
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

def find_nn(np.ndarray[double, ndim=2, mode="c"] psouLat not None,
            np.ndarray[double, ndim=2, mode="c"] psouLon not None,
            int nSou,
            np.ndarray[double, ndim=2, mode="c"] tarLat not None,
            np.ndarray[double, ndim=2, mode="c"] tarLon not None,
            np.ndarray[int, ndim=1, mode="c"] tarNNSouID not None,        
            np.ndarray[double, ndim=2, mode="c"] tarNNDis not None,
            int nTar, double maxR):
    
    # See [1] for handling double pointers. 
    cdef double* pLat = &psouLat[0,0]
    cdef double* pLon = &psouLon[0,0]
    
    nearestNeighbor(&pLat, &pLon, nSou,
                    &tarLat[0,0], &tarLon[0,0], &tarNNSouID[0],
                    &tarNNDis[0,0], nTar, maxR)    
        
def find_nn_block_index(
        np.ndarray[double, ndim=2, mode="c"] psouLat not None,
        np.ndarray[double, ndim=2, mode="c"] psouLon not None,
        int nSou,
        np.ndarray[double, ndim=2, mode="c"] tarLat not None,
        np.ndarray[double, ndim=2, mode="c"] tarLon not None,
        np.ndarray[int, ndim=1, mode="c"] tarNNSouID not None,        
        np.ndarray[double, ndim=2, mode="c"] tarNNDis not None,
        int nTar, double maxR):
    
    # See [1] for handling double pointers. 
    cdef double* pLat = &psouLat[0,0]
    cdef double* pLon = &psouLon[0,0]
    
    nearestNeighborBlockIndex(&pLat, &pLon, nSou,
                              &tarLat[0,0], &tarLon[0,0], &tarNNSouID[0],
                              &tarNNDis[0,0], nTar, maxR)
    return None

def interpolate_nn(np.ndarray[double, ndim=2, mode="c"] souVal not None,
                   np.ndarray[double, ndim=2, mode="c"] tarVal not None,
                   np.ndarray[int, ndim=1, mode="c"] tarNNSouID not None,
                   int nTar):
    nnInterpolate(&souVal[0,0], &tarVal[0,0], &tarNNSouID[0], nTar)
    return None

def interpolate_summary(np.ndarray[double, ndim=2, mode="c"] souVal not None,
                        np.ndarray[int, ndim=1, mode="c"] souNNSouID not None,
                        int nSou,
                        np.ndarray[double, ndim=2, mode="c"] tarVal not None,
                        np.ndarray[double, ndim=2, mode="c"] tarSD not None,
                        np.ndarray[int, ndim=1, mode="c"] nSouPixels not None,
                        int nTar):
    summaryInterpolate(&souVal[0,0], &souNNSouID[0], nSou,
                       &tarVal[0,0], &tarSD[0,0], &nSouPixels[0], nTar)
    return None

# Wrapper for getting the target values.
def resample(np.ndarray[double, ndim=2, mode="c"] psouLat not None,
             np.ndarray[double, ndim=2, mode="c"] psouLon not None,
             np.ndarray[double, ndim=2, mode="c"] ptarLat not None,
             np.ndarray[double, ndim=2, mode="c"] ptarLon not None,             
             np.ndarray[double, ndim=2, mode="c"] psouVal not None,
             ):
    # Get the shape of lat/lon [2].
    nx = ptarLat.shape[0]
    ny = ptarLat.shape[1]
    trg_data = np.arange(nx*ny, dtype=np.float64).reshape((ny,nx))
    
    return trg_data

# Wrapper for summary.
def resample_s(np.ndarray[double, ndim=2, mode="c"] psouLat not None,
               np.ndarray[double, ndim=2, mode="c"] psouLon not None,
               np.ndarray[double, ndim=2, mode="c"] ptarLat not None,
               np.ndarray[double, ndim=2, mode="c"] ptarLon not None,
               np.ndarray[double, ndim=2, mode="c"] psouVal not None,
             ):
    nx = ptarLat.shape[0]
    ny = ptarLat.shape[1]
    trg_data = np.arange(nx*ny, dtype=np.float64).reshape((ny,nx))
    
    return trg_data

# References
#
# [1] https://stackoverflow.com/questions/40413858/how-to-handle-double-pointer-in-c-wrapping-by-cython
# [2] https://github.com/cython/cython/wiki/tutorials-NumpyPointerToC
