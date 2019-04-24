from unittest import TestCase

import pytaf
import numpy as np

class TestClip(TestCase):

    def test_clip(self):
        a = np.arange(12, dtype=np.float64).reshape((3,4))
        b = a * -333
        # If mask[i] is -999, value[i] becomes -999
        pytaf.clip(a, b, 4)
        c = np.arange(12, dtype=np.float64).reshape((3,4))
        c[0][3] = -999.
        try:
            np.testing.assert_array_equal(a, c)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
