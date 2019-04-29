from unittest import TestCase

import pytaf
import numpy as np

class TestGetSourceList(TestCase):

    def test_get_source_list(self):
        slat = np.arange(12, dtype=np.float64).reshape((3,4))
        slon = np.arange(12, dtype=np.float64).reshape((3,4))        
        sdata = np.arange(12, dtype=np.float64).reshape((3,4))
        r = 555
        tlat = 5.5
        tlon = 5.5
        a, b, c, d = pytaf.get_source_list(slat, slon, sdata, r, tlat, tlon)
        try:
            np.testing.assert_almost_equal(a, [], decimal=8)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
