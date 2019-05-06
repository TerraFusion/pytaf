from unittest import TestCase

import pytaf
import numpy as np


class TestResampleNS(TestCase):

    # Both source and target are 1-d.
    def test_resample_n_1d_s(self):
        slat= np.array([30,33,36,39],dtype=np.float64)
        slon= np.array([40,43,46,49],dtype=np.float64)
        tlat= np.array([40,37,34,31],dtype=np.float64)
        tlon= np.array([50,47,44,41],dtype=np.float64)
        sdata=np.array([1,2,3,4],dtype=np.float64)
        #radius 150 km(about the distance between (30,40) and(31,41))
        r = 150000.
        g = pytaf.resample_n(slat, slon, tlat, tlon, sdata, r)
        h = np.array([4,3,2,1])
        try:
            np.testing.assert_array_equal(g, h)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    # Both source and target are 2-d.
    def test_resample_n_2d_s(self):
        slat= np.array([30,33,36,39],dtype=np.float64).reshape((2,2))
        slon= np.array([40,43,46,49],dtype=np.float64).reshape((2,2))
        tlat= np.array([40,37,34,31],dtype=np.float64).reshape((2,2))
        tlon= np.array([50,47,44,41],dtype=np.float64).reshape((2,2))
        sdata=np.array([1,2,3,4],dtype=np.float64).reshape((2,2))
        #radius 150 km(about the distance between (30,40) and(31,41))
        r = 150000.
        g = pytaf.resample_n(slat, slon, tlat, tlon, sdata, r)
        h = np.array([[4,3], 
                      [2,1]])
        try:
            np.testing.assert_array_equal(g, h)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

