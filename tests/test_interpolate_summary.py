from unittest import TestCase

import pytaf
import numpy as np

class TestInterpolateSummary(TestCase):

    def test_interpolate_summary(self):
        sdata = np.arange(12, dtype=np.float64).reshape((3,4))
        tdata = np.zeros((3,4), dtype=np.float64)
        i = np.arange(12, dtype=np.int32)
        sd = np.arange(12, dtype=np.float64).reshape((3,4))
        npix = np.arange(12, dtype=np.int32).reshape((3,4))        
        pytaf.interpolate_summary(sdata, i, sdata.size, tdata, sd, npix,
                                  tdata.size)
        try:
            h = sdata
            h[0][0] = -999.0
            np.testing.assert_almost_equal(tdata, h, decimal=8)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
