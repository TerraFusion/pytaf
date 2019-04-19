from unittest import TestCase

import pytaf
import numpy as np


class TestResampleN(TestCase):
    
    def test_resample_n_1d(self):
        slat = np.arange(12, dtype=np.float64)
        slon = np.arange(12, dtype=np.float64)
        sdata = slat * -333
        tlat = np.arange(12, dtype=np.float64)
        tlon = np.arange(12, dtype=np.float64)
        # radius
        r = 5555
        g = pytaf.resample_n(slat, slon, tlat, tlon, sdata, r)
        h = np.array([-0.,  -333.,  -666.,  -999., 
                      -1332., -1665., -1998.,-2331.,
                      -999., -2997.,  -3330., -3663.])
        try:
            np.testing.assert_array_equal(g, h)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
        # Use the following if you don't want to use numpy.testing.
        # self.assertEqual(g.tolist(), h.tolist())
