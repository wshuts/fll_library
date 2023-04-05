import unittest
from band_edge_filter import BandEdgeFilter


class TestBandEdgeFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.samps_per_sym = 16.0
        self.filter_size = 321
        self.alpha = 0.5

        self.band_edge_filter = BandEdgeFilter(self.samps_per_sym, self.filter_size, self.alpha)
        self.band_edge_filter.design()

        return

    def test_constructor(self):
        samps_per_sym_actual = self.band_edge_filter.samps_per_sym
        filter_size_actual = self.band_edge_filter.filter_size
        alpha_actual = self.band_edge_filter.alpha

        samps_per_sym_expected = self.samps_per_sym
        filter_size_expected = self.filter_size
        alpha_expected = self.alpha

        self.assertEqual(samps_per_sym_expected, samps_per_sym_actual)
        self.assertEqual(filter_size_expected, filter_size_actual)
        self.assertEqual(alpha_expected, alpha_actual)

    def test_symbol_times(self):
        leftmost_index = 0
        center_index = round(0.5 * (self.filter_size - 1))
        rightmost_index = self.filter_size - 1

        leftmost_actual = self.band_edge_filter.symbol_times[leftmost_index]
        center_actual = self.band_edge_filter.symbol_times[center_index]
        rightmost_actual = self.band_edge_filter.symbol_times[rightmost_index]

        leftmost_expected = -1 * self.alpha * (self.filter_size - 1) / self.samps_per_sym
        center_expected = 0.0
        rightmost_expected = 1 * self.alpha * (self.filter_size - 1) / self.samps_per_sym

        self.assertEqual(leftmost_expected, leftmost_actual)
        self.assertEqual(center_expected, center_actual)
        self.assertEqual(rightmost_expected, rightmost_actual)

    def test_bb_taps(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)
        band_edge_filter.design()

        zero_left = band_edge_filter.bb_taps[160 - 8 - 16]
        peak_left = band_edge_filter.bb_taps[160 - 8]
        peak_right = band_edge_filter.bb_taps[160 + 8]
        zero_right = band_edge_filter.bb_taps[160 + 8 + 16]

        self.assertEqual(zero_left, 0.0)
        self.assertEqual(peak_left, 1.0)
        self.assertEqual(peak_right, 1.0)
        self.assertEqual(zero_right, 0.0)

    def test_power(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)
        band_edge_filter.design()

        power = band_edge_filter.power

        self.assertAlmostEqual(power, 32.0, 2)

    def tearDown(self) -> None:
        self.band_edge_filter.dispose()
        return


if __name__ == '__main__':
    unittest.main()
