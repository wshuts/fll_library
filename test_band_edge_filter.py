import unittest
from band_edge_filter import BandEdgeFilter


class TestBandEdgeFilter(unittest.TestCase):

    def test_constructor(self):
        samps_per_sym = 16.0
        filter_size = 321
        alpha = 0.5

        band_edge_filter = BandEdgeFilter(samps_per_sym, filter_size, alpha)

        samps_per_sym_actual = band_edge_filter.samps_per_sym
        filter_size_actual = band_edge_filter.filter_size
        alpha_actual = band_edge_filter.alpha

        samps_per_sym_expected = samps_per_sym
        filter_size_expected = filter_size
        alpha_expected = alpha

        self.assertEqual(samps_per_sym_expected, samps_per_sym_actual)
        self.assertEqual(filter_size_expected, filter_size_actual)
        self.assertEqual(alpha_expected, alpha_actual)

    def test_symbol_times(self):
        samps_per_sym = 16.0
        filter_size = 321
        alpha = 0.5

        leftmost_index = 0
        center_index = round(0.5 * (filter_size - 1))
        rightmost_index = filter_size - 1

        band_edge_filter = BandEdgeFilter(samps_per_sym, filter_size, alpha)
        band_edge_filter.design()

        leftmost_actual = band_edge_filter.symbol_times[leftmost_index]
        center_actual = band_edge_filter.symbol_times[center_index]
        rightmost_actual = band_edge_filter.symbol_times[rightmost_index]

        leftmost_expected = -1 * alpha * (filter_size - 1) / samps_per_sym
        center_expected = 0.0
        rightmost_expected = 1 * alpha * (filter_size - 1) / samps_per_sym

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


if __name__ == '__main__':
    unittest.main()
