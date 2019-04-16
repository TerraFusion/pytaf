"""
pytaf.pyx

simple cython test of accessing advancedFusion functions

The C functions from advancedFusion:

 * reproject.cpp/clipping 
 * reproject.cpp/nnInterpolate
 ...

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-16
"""
import numpy as np
cimport cython

# import both numpy and the Cython declarations for numpy
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
    
@cython.boundscheck(False)
@cython.wraparound(False)        
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
                        np.ndarray[int, ndim=2, mode="c"] nSouPixels not None,
                        int nTar):
    summaryInterpolate(&souVal[0,0], &souNNSouID[0], nSou,
                       &tarVal[0,0], &tarSD[0,0], &nSouPixels[0,0], nTar)
    return None

# Check dimensions if src/trg lat/lon dimensions are 1 or 2.
def check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
    # Return error if dimension size is not 2.
    if psouLat.ndim < 1 or psouLat.ndim > 2:
        print('No. of source latitude dimensions should be 1 or 2.')
        return False
    if psouLat.ndim < 1 or psouLon.ndim > 2:
        print('No. of source longitude dimensions should be 1 or 2.')
        return False
    if ptarLat.ndim < 1 or ptarLat.ndim > 2:
        print('No. of target latitude dimensions should be 1 or 2.')
        return False
    if ptarLon.ndim < 1 or ptarLon.ndim > 2:
        print('No. of target longitude dimensions should be 1 or 2.')
        return False
    if ptarLat.ndim != ptarLon.ndim:
        print('Target lat/lon dimension sizes do not match.')
        print('Lat dim = '+str(ptarLat.ndim))
        print('Lon dim = '+str(ptarLon.ndim))        
        return False
    if psouLat.ndim != psouLon.ndim:
        print('Source lat/lon dimension sizes do not match.')
        print('Lat dim = '+str(psouLat.ndim))
        print('Lon dim = '+str(psouLon.ndim))        
        return False    
    return True

# Wrapper for any projection using nn interpolation.
def resample_n(psouLat, psouLon, ptarLat, ptarLon, psouVal, r):
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        # Default - all 2d
        slon = psouLon
        slat = psouLat
        tlon = ptarLon
        tlat = ptarLat
        sval = psouVal
        
        # If source is 1d lat/lon, reshape source value.
        if psouLat.ndim == 1:
            # Generate 2d lat/lon.
            print("generating 2d source lat/lon/src values...")            
            slat = psouLat.reshape(psouLat.size, 1)
            slon = psouLon.reshape(psouLon.size, 1)
            sval= psouLon.reshape(psouVal.size, 1)
        # If target is 1d lat/lon, return value is also 1d.            
        if ptarLat.ndim == 1:
            print("generating 2d target lat/lon values...")            
            tlat = ptarLat.reshape(ptarLat.size, 1)
            tlon = ptarLon.reshape(ptarLon.size, 1)
            trg = resample(slat, slon, tlat, tlon, sval, r)
            return trg.ravel()
        else:
            return resample(slat, slon, tlat, tlon, sval, r)
    else:
        return None
    
# Wrapper for geographic projection using nn interpolation.
def resample_n_g(psouLat, psouLon, ptarLat, ptarLon, psouVal, r):
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        if ptarLat.ndim == 1:
            # Generate 2d lat/lon.
            lat, lon = np.meshgrid(ptarLon, ptarLat)
            latd = np.array(lat, dtype='float64')
            lond = np.array(lon, dtype='float64')
            return resample(psouLat, psouLon,
                            latd, lond,
                            psouVal, r)
        else:
            return resample(psouLat, psouLon, ptarLat, ptarLon, psouVal, r)
    else:
        return None
    
# Wrapper for any projection using summary interpolation.
def resample_s(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
               tarSD, nSouPixels):
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        if psouLat.ndim == 1:
            # Generate 2d lat/lon.
            print("generating 2d lat/lon...")
            latd = psouLat.reshape(psouLat.size, 1)
            lond = psouLon.reshape(psouLon.size, 1)
            
            return resample(latd, lond,
                            ptarLat, ptarLon,
                            psouVal, r, True, tarSD, nSouPixels)
        else:
            return resample(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
                             True, tarSD, nSouPixels)
    else:
        return None
    
# Wrapper for geographic projection using summary interpolation.
def resample_s_g(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
                 tarSD, nSouPixels):
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        if ptarLat.ndim == 1:
            # Generate 2d lat/lon.
            lat, lon = np.meshgrid(ptarLat, ptarLon)
            latd = np.array(lat, dtype='float64')
            lond = np.array(lon, dtype='float64')
            # latd = lat_.copy()
            # lond = lon_.copy()
            print("generating 2d lat/lon...")
            return resample(psouLat, psouLon,
                            latd, lond,
                            psouVal, r, True, tarSD, nSouPixels)
        else:
            return resample(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
                            True, tarSD, nSouPixels)
    else:
        return None

# Wrapper for getting the target values.
def resample(psouLat, psouLon, ptarLat, ptarLon, psouVal,
             r, s=False, tarSD=None, nSouPixels=None):
    # Get the shape of lat/lon [2].
    nx = ptarLat.shape[1]
    # print(nx)
    ny = ptarLat.shape[0]
    # print(ny)
    n_trg = nx * ny;
    # print(n_trg)
    if s is True:
        print('using summary interpolation')
        if tarSD is None:
            print('Target std. dev. input is None.')
            return None
        if nSouPixels is None:
            print('Source no. pixel input is None')
            return None
        
        trg_data = np.zeros((ny,nx), dtype=psouVal.dtype)        
        n_src = psouLat.size;
        print(n_src)
        sx = psouLat.shape[0]
        print(sx)
        sy = psouLat.shape[1]
        print(sy)
        i = np.arange(n_src, dtype=np.int32)
        d = np.arange(n_src, dtype=np.float64).reshape((sy,sx))
        # tlat = ptarLat.copy()
        # tlon = ptarLon.copy()
        # slat = psouLat.copy()
        # slon = psouLon.copy()
        find_nn_block_index(ptarLat, ptarLon,
#        find_nn_block_index(tlat, tlon,
                            n_trg,
                            psouLat, psouLon,
#                            slat, slon,
                            i, d,
                            n_src,
                            r)
        print('finished generating index.')
        # print(index)
        interpolate_summary(psouVal, i, n_src,
                            trg_data, tarSD, nSouPixels, n_trg)
        print('finished retrieving data with index.')
        return trg_data
    else:
        print('using nn interpolation')
        trg_data = np.zeros((ny,nx), dtype=psouVal.dtype)        
        i = np.arange(nx*ny, dtype=np.int32)
        d = np.arange(nx*ny, dtype=np.float64).reshape((ny,nx))        
        find_nn_block_index(psouLat, psouLon,
                            psouLat.size,
                            ptarLat, ptarLon,
                            i, d,
                            n_trg,
                            r)
        interpolate_nn(psouVal, trg_data, i, n_trg)
        return trg_data
# References
#
# [1] https://stackoverflow.com/questions/40413858/how-to-handle-double-pointer-in-c-wrapping-by-cython
# [2] https://github.com/cython/cython/wiki/tutorials-NumpyPointerToC
# [3] https://stackoverflow.com/questions/51546710/pass-data-from-a-c-function-via-double-pointer-in-cython
