from unittest import TestCase

import pytaf
import numpy as np

class TestInterpolateNN(TestCase):

    def test_interpolate_nn(self):
        sdata = np.arange(12, dtype=np.float64).reshape((3,4))
        tdata = np.zeros((3,4), dtype=np.float64)
        i = np.arange(12, dtype=np.int32)
        pytaf.interpolate_nn(sdata, tdata, i, 12)
        try:
            np.testing.assert_almost_equal(sdata, tdata, decimal=8)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
