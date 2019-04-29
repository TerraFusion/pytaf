from unittest import TestCase

import pytaf
import numpy as np


class TestResampleS(TestCase):
    tsd = np.arange(12, dtype=np.float64).reshape((3,4))
    npix = np.arange(12, dtype=np.int32).reshape((3,4))
    r = 555
    # Both source and target are 1-d.
    def test_resample_s_1d(self):
        slat = np.arange(12, dtype=np.float64)
        slon = np.arange(12, dtype=np.float64)
        sdata = slat * -333
        tlat = np.arange(12, dtype=np.float64)
        tlon = np.arange(12, dtype=np.float64)
        tsd1 = np.arange(12, dtype=np.float64)
        npix1 = np.arange(12, dtype=np.int32)
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, tsd1, npix1)
        h = np.array([0., -999., -999., -999., -999., -999., -999., -999.,
                      -999., -999., -999., -999.])
        j = np.array([1, 0, 0, 0,
                      0, 0, 0, 0,
                      0, 0, 0, 0])
        try:
            np.testing.assert_almost_equal(g, h)
            np.testing.assert_almost_equal(tsd1, h)
            np.testing.assert_almost_equal(npix1, j)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    # Both source and target are 2-d.
    def test_resample_s_2d(self):
        slat = np.arange(12, dtype=np.float64).reshape((3,4))
        slon = np.arange(12, dtype=np.float64).reshape((3,4))
        sdata = slat * -333
        tlat = np.arange(12, dtype=np.float64).reshape((3,4))
        tlon = np.arange(12, dtype=np.float64).reshape((3,4))
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, self.tsd, self.npix)
        h = np.array(
            [[0., -999., -999., -999.],
             [-999., -999., -999., -999.],
             [-999., -999., -999., -999.]])
        try:
            np.testing.assert_almost_equal(g, h)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    # Source is 2-d and target is 1-d.
    def test_resample_s_2d_to_1d(self):
        slat = np.arange(12, dtype=np.float64).reshape((3,4))
        slon = np.arange(12, dtype=np.float64).reshape((3,4))
        sdata = slat * -333
        tlat = np.arange(12, dtype=np.float64)
        tlon = np.arange(12, dtype=np.float64)
        tsd1 = np.arange(12, dtype=np.float64)
        npix1 = np.arange(12, dtype=np.int32)
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, tsd1, npix1)
        h = np.array([0., -999., -999., -999., -999., -999., -999., -999.,
                      -999.,-999., -999., -999.])
        j = np.zeros(12)
        j[0] = 1
        try:
            np.testing.assert_almost_equal(g, h)
            np.testing.assert_almost_equal(tsd1, h)
            np.testing.assert_almost_equal(npix1, j)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    # Source is 1-d and target is 2-d.
    def test_resample_s_1d_to_2d(self):
        slat = np.arange(12, dtype=np.float64)
        slon = np.arange(12, dtype=np.float64)
        sdata = slat * -333
        tlat = np.arange(12, dtype=np.float64).reshape((3,4))
        tlon = np.arange(12, dtype=np.float64).reshape((3,4))
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, self.tsd, self.npix)
        h = np.array(
            [[   0., -999., -999., -999.],
             [-999., -999., -999., -999.],
             [-999., -999., -999., -999.]])
        try:
            np.testing.assert_almost_equal(g, h)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
        
