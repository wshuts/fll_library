import unittest
from band_edge_filter import BandEdgeFilter


class TestBandEdgeFilter(unittest.TestCase):

    def test_constructor(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)

        samps_per_sym = band_edge_filter.samps_per_sym
        filter_size = band_edge_filter.filter_size
        rolloff = band_edge_filter.rolloff

        self.assertEqual(samps_per_sym, 16.0)
        self.assertEqual(filter_size, 321)
        self.assertEqual(rolloff, 0.5)


if __name__ == '__main__':
    unittest.main()
