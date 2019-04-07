#!/usr/bin/env python3
import numpy as np
import lut2d
import sys
import imageio

if len(sys.argv) != 2:
    print('usage:', sys.argv[0], 'some-lut.txt')
filename = sys.argv[1]

lut = np.loadtxt(filename, dtype='uint8')

size = 128
img = np.random.randint(0, 2, (size, size), dtype='uint8')

steps = 70
for i in range(steps):
    imageio.imwrite('lut-step%05d.png' % i, img * 255, compress_level=6)
    img = lut2d.binary_lut_filter(img, lut)
