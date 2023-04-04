import unittest

from verifier import Verifier
from filter import Filter


class TestVerifier(unittest.TestCase):
    def test_center_tap(self):

        band_edge_filter = Filter()
        band_edge_filter.design_filter(16, 0.5, 321)
        center_tap_designed = band_edge_filter.d_taps_upper[160]

        verifier = Verifier()
        verifier.load_coefficients()
        verifier.de_rotate_coefficients()
        center_tap_verified = verifier.center_tap

        self.assertAlmostEqual(center_tap_verified, center_tap_designed, 15)  # add assertion here


if __name__ == '__main__':
    unittest.main()
