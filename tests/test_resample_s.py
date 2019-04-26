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
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, self.tsd, self.npix)
        h = np.array([-9.990000e+02,  1.745329e-02,  3.490659e-02,
                      5.235988e-02, 6.981317e-02,  8.726646e-02,
                      1.047198e-01,  1.221730e-01, -9.990000e+02,
                      1.570796e-01,  1.745329e-01,  1.919862e-01])
        try:
            np.testing.assert_almost_equal(g, h)
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
            [[-999., -999., -999., -999.],
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
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, self.tsd, self.npix)
        h = np.array([-999., -999., -999., -999., -999., -999., -999., -999.,
                      -999.,-999., -999., -999.])
        try:
            np.testing.assert_almost_equal(g, h)
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
            [[-9.9900000e+02,  1.7453293e-02,  3.4906585e-02,  5.2359878e-02],
             [ 6.9813170e-02,  8.7266463e-02,  1.0471976e-01,  1.2217305e-01],
             [-9.9900000e+02,  1.5707963e-01,  1.7453293e-01,  1.9198622e-01]])
        try:
            np.testing.assert_almost_equal(g, h)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
        
