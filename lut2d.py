from numba import guvectorize
import numpy as np

"""Filter a 2d binary image using a hex neighbours+center LUT.

Using periodic boundary conditions.
Input pixels are assumed to be {0, 1} of type uint8.
The 7-bit LUT is given as uint8 array of length 2^7.
"""
def binary_lut_filter(inp, lut):
    assert len(lut) == 2**7, 'LUT must have 2^7 entries'
    result = np.zeros_like(inp)
    binary_lut_filter_inner(inp, lut, result)
    # print(binary_lut_filter_inner.inspect_types())
    return result


# measured to be just 1.5x slower than the same written C
@guvectorize(["void(uint8[:,:], uint8[:], uint8[:,:])"],
             "(n,n),(k)->(n,n)", nopython=True)
def binary_lut_filter_inner(src, lut, result):
    # everything except borders
    h = src.shape[0]
    w = src.shape[1]
    for y in range(1, h-1):
        for x in range(1, w-1):
            key = 0
            key |= (src[y-1, x+0] & 1) << 0
            key |= (src[y-1, x+1] & 1) << 1
            key |= (src[y+0, x-1] & 1) << 2
            key |= (src[y+0, x+0] & 1) << 3
            key |= (src[y+0, x+1] & 1) << 4
            key |= (src[y+1, x-1] & 1) << 5
            key |= (src[y+1, x+0] & 1) << 6
            result[y, x] = lut[key]
