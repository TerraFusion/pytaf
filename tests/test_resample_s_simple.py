from unittest import TestCase

import pytaf
import numpy as np


class TestResampleS_S(TestCase):
    #radius 100 km(make sure the point separated from(30.5,40.5),(31.5,41.5))
    r = 100000.
    # Both source and target are 1-d.
    def test_resample_s_1d_s(self):
        slat = np.array([30.5,31.5,32.5,33.5,36.5,37.5,38.5,39.5],dtype=np.float64)
        slon = np.array([40.5,41.5,42.5,43.5,46.5,47.5,48.5,49.5],dtype=np.float64)
        tlat = np.array([39,37,33,31],dtype=np.float64)
        tlon = np.array([49,47,43,41],dtype=np.float64)
        sdata=np.array([1,3,5,7,9,11,13,15],dtype=np.float64)
        sd = np.arange(4, dtype=np.float64)
        pc = np.arange(4, dtype=np.int32)

        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata, self.r,sd,pc)

        h = np.array([14,10,6,2],dtype=np.float64)
        
        pc1 = np.array([2,2,2,2],dtype=np.float64)
        sd1 = np.array([1,1,1,1],dtype=np.float64)
        try:
            np.testing.assert_array_equal(g, h)
            np.testing.assert_array_equal(sd1, sd)
            np.testing.assert_array_equal(pc1, pc)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    # Both source and target are 2-d.
    def test_resample_s_2d_s(self):
        slat = np.array([30.5,31.5,32.5,33.5,36.5,37.5,38.5,39.5],dtype=np.float64).reshape(4,2)
        slon = np.array([40.5,41.5,42.5,43.5,46.5,47.5,48.5,49.5],dtype=np.float64).reshape(4,2)
        tlat = np.array([39,37,33,31],dtype=np.float64).reshape(2,2)
        tlon = np.array([49,47,43,41],dtype=np.float64).reshape(2,2)
        sdata=np.array([1,3,5,7,9,11,13,15],dtype=np.float64).reshape(4,2)
        sd = np.arange(4, dtype=np.float64).reshape(2,2)
        pc = np.arange(4, dtype=np.int32).reshape(2,2)
        pc1 = np.array([2,2,2,2],dtype=np.float64).reshape(2,2)
        sd1 = np.array([1,1,1,1],dtype=np.float64).reshape(2,2)
        g = pytaf.resample_s(slat, slon, tlat, tlon, sdata,
                             self.r, sd, pc)
        h = np.array(
            [[14,10],
             [6,2]]);
        try:
            np.testing.assert_array_equal(g, h)
            np.testing.assert_array_equal(sd, sd1)
            np.testing.assert_array_equal(pc, pc1)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

        
