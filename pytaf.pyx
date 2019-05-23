"""
pytaf.pyx

A simple Cython-based Python wrapper for accessing advancedFusion functions

The C functions are from advancedFusion:

 * reproject.c/clipping 
 * reproject.c/nnInterpolate
 * ...
 * etc.

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-19
"""
import numpy as np
cimport cython

# Import both numpy and the Cython declarations for numpy.
cimport numpy as np

# Declare the interface to the C code.
cdef extern void clipping(double * val, double * mask, int nPixels)
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
    clipping(& val[0, 0], & mask[0, 0], nPixels)
    return None


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
    """Find the nearest neighboring source cell's index for each target cell."""
    cdef double * pLat = &psouLat[0, 0]
    cdef double * pLon = &psouLon[0, 0]
    nearestNeighborBlockIndex(& pLat, & pLon, nSou,
                              & tarLat[0, 0], & tarLon[0, 0], & tarNNSouID[0],
                              & tarNNDis[0, 0], nTar, maxR)
    return None


def interpolate_nn(np.ndarray[double, ndim=2, mode="c"] souVal not None,
                   np.ndarray[double, ndim=2, mode="c"] tarVal not None,
                   np.ndarray[int, ndim=1, mode="c"] tarNNSouID not None,
                   int nTar):
    """ Nearest neighbor interpolation """
    nnInterpolate( & souVal[0, 0], & tarVal[0, 0], & tarNNSouID[0], nTar)
    return None


def interpolate_summary(np.ndarray[double, ndim=2, mode="c"] souVal not None,
                        np.ndarray[int, ndim=1, mode="c"] souNNSouID not None,
                        int nSou,
                        np.ndarray[double, ndim=2, mode="c"] tarVal not None,
                        np.ndarray[double, ndim=2, mode="c"] tarSD not None,
                        np.ndarray[int, ndim=2, mode="c"] nSouPixels not None,
                        int nTar):
    """ Interpolation (summary) from fine resolution to coarse resolution. """
    summaryInterpolate( & souVal[0, 0], & souNNSouID[0], nSou,
                        & tarVal[0, 0], & tarSD[0, 0], & nSouPixels[0, 0], nTar)
    return None

def check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
    """ Check dimensions if src/trg lat/lon dimensions are 1 or 2. """
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

def resample_n(psouLat, psouLon, ptarLat, ptarLon, psouVal, r):
    """ Wrapper for any projection using nn interpolation. """
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        # Default - all 2D
        slon = psouLon
        slat = psouLat
        tlon = ptarLon
        tlat = ptarLat
        sval = psouVal

        if psouLat.ndim == 1:
            # Generate 2D lat/lon.
            slat = psouLat.reshape(psouLat.size, 1)
            slon = psouLon.reshape(psouLon.size, 1)
            # If source is 1D lat/lon, make source value 2D.
            sval = psouVal.reshape(psouVal.size, 1)
        if ptarLat.ndim == 1:
            tlat = ptarLat.reshape(ptarLat.size, 1)
            tlon = ptarLon.reshape(ptarLon.size, 1)
            trg = resample(slat, slon, tlat, tlon, sval, r)
            # If target is 1D lat/lon, return value should be 1D.
            return trg.ravel()
        else:
            return resample(slat, slon, tlat, tlon, sval, r)
    else:
        return None

def resample_n_g(psouLat, psouLon, ptarLat, ptarLon, psouVal, r):
    """ Wrapper for geographic projection using nn interpolation. """
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        if ptarLat.ndim == 1:
            # Generate 2D lat/lon.
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

def resample_s(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
               tarSD, nSouPixels):
    """ Wrapper for any projection using summary interpolation. """
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        # Default - all 2D
        slon = psouLon
        slat = psouLat
        tlon = ptarLon
        tlat = ptarLat
        sval = psouVal
        tstd = tarSD
        tnpx = nSouPixels
        
        if psouLat.ndim == 1:
            # Generate 2D lat/lon.
            slat = psouLat.reshape(psouLat.size, 1)
            slon = psouLon.reshape(psouLon.size, 1)
            sval = psouVal.reshape(psouVal.size, 1)
        if ptarLat.ndim == 1:
            tlat = ptarLat.reshape(ptarLat.size, 1)
            tlon = ptarLon.reshape(ptarLon.size, 1)
            tstd = tarSD.reshape(tarSD.size, 1)
            tnpx = nSouPixels.reshape(nSouPixels.size, 1)
            trg = resample(slat, slon, tlat, tlon, sval, r,
                           True, tstd, tnpx)
            # If target is 1D lat/lon, return value should be 1D.
            return trg.ravel()
        else:
            return resample(slat, slon, tlat, tlon, sval, r,
                            True, tstd, tnpx)
    else:
        return None

def resample_s_g(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
                 tarSD, nSouPixels):
    """ Wrapper for geographic projection using summary interpolation. """
    if check_dimensions(psouLat, psouLon, ptarLat, ptarLon, psouVal):
        if ptarLat.ndim == 1:
            # Generate 2D lat/lon.
            lat, lon = np.meshgrid(ptarLat, ptarLon)
            latd = np.array(lat, dtype='float64')
            lond = np.array(lon, dtype='float64')
            return resample(psouLat, psouLon,
                            latd, lond,
                            psouVal, r, True, tarSD, nSouPixels)
        else:
            return resample(psouLat, psouLon, ptarLat, ptarLon, psouVal, r,
                            True, tarSD, nSouPixels)
    else:
        return None

def resample(psouLat, psouLon, ptarLat, ptarLon, psouVal,
             r, s=False, tarSD=None, nSouPixels=None):
    """ Wrapper for getting the target values. """
    nx = ptarLat.shape[1]
    ny = ptarLat.shape[0]
    n_trg = nx * ny

    if s is True:
        if tarSD is None:
            print('Target std. dev. input is None.')
            return None
        if nSouPixels is None:
            print('Source no. pixel input is None')
            return None

        trg_data = np.zeros((ny, nx), dtype=psouVal.dtype)
        n_src = psouLat.size
        sx = psouLat.shape[0]
        sy = psouLat.shape[1]
        i = np.arange(n_src, dtype=np.int32)
        d = np.arange(n_src, dtype=np.float64).reshape((sy, sx))
        find_nn_block_index(ptarLat, ptarLon,
                            n_trg,
                            psouLat, psouLon,
                            i, d,
                            n_src,
                            r)
        interpolate_summary(psouVal, i, n_src,
                            trg_data, tarSD, nSouPixels, n_trg)
        return trg_data
    else:
        trg_data = np.zeros((ny, nx), dtype=psouVal.dtype)
        i = np.arange(nx*ny, dtype=np.int32)
        d = np.arange(nx*ny, dtype=np.float64).reshape((ny, nx))
        find_nn_block_index(psouLat, psouLon,
                            psouLat.size,
                            ptarLat, ptarLon,
                            i, d,
                            n_trg,
                            r)
        interpolate_nn(psouVal, trg_data, i, n_trg)
        return trg_data
