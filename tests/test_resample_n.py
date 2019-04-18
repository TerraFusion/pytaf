from unittest import TestCase

import pytaf

class TestResampleN(TestCase):
    def test_is_string(self):
        g = pytaf.resample_n()
        self.assertTrue(g)
