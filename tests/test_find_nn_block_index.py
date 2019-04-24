from unittest import TestCase

import pytaf
import numpy as np

class TestFindNNBlockIndex(TestCase):

    def test_find_nn_block_index(self):
        slat = np.arange(12, dtype=np.float64).reshape((3,4))
        slon = np.arange(12, dtype=np.float64).reshape((3,4))
        sdata = slat * -333
        tlat = np.arange(12, dtype=np.float64).reshape((3,4))
        tlon = np.arange(12, dtype=np.float64).reshape((3,4))
        r = 5555
        distance = np.arange(12, dtype=np.float64).reshape((3,4))
        index = np.arange(12, dtype=np.int32)
        pytaf.find_nn_block_index(slat, slon, sdata.size, tlat, tlon,
                                  index, distance, tlat.size, r)
        index_o = np.arange(12, dtype=np.int32)
        index_o[8] = -1
        # distnace_o[8] must be -1.0
        distance_o = [[ 0.,  0.,  0.,  0.09488231],
                      [ 0.09488231,  0.,  0.09488231,  0.09488231],
                      [-1.,  0.,  0.09488231,  0.]]
        try:
            np.testing.assert_array_equal(index, index_o)
            np.testing.assert_almost_equal(distance, distance_o, decimal=8)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
