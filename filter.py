from numpy import sinc
#  port from GNU Radio fll_band_edge_cc_impl

# /* -*- c++ -*- */
# /*
#  * Copyright 2009-2012,2014 Free Software Foundation, Inc.
#  *
#  * This file is part of GNU Radio
#  *
#  * SPDX-License-Identifier: GPL-3.0-or-later
#  *
#  */


def design_filter(samps_per_sym: float, rolloff: float, filter_size: int):
    m = round(filter_size / samps_per_sym)
    power = 0
    bb_taps = []

    # Create the baseband filter by adding two sincs together
    tap_index = range(0, filter_size)
    for i in tap_index:
        k = -m + i * 2.0 / samps_per_sym
        tap = sinc(rolloff * k - 0.5) + sinc(rolloff * k + 0.5)
        power += tap

        bb_taps.append(tap)
    return
