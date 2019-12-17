#!/usr/bin/env python3
import numpy as np
import scipy.special as sc
import imageio
import time
import lut2d
import render

target_edge_count = 0.05
target_brigthness = 0.45
filter_steps = 8
size = 64 + 2*filter_steps

def generate_image(lut, count=filter_steps):
    # generate binary noise image
    img = np.random.randint(0, 2, (size, size), dtype='uint8')
    # apply the lut as filter several times
    for j in range(count):
        img = lut2d.binary_lut_filter(img, lut)
    return img

def make_edge_detection_lut(neighbour):
    neighbour_mask = 1<<neighbour
    center_mask = 1<<3
    lut = np.zeros(2**7, dtype='uint8')
    for key in range(2**7):
        if bool(key & center_mask) != bool(key & neighbour_mask):
            lut[key] = 1
    return lut

edge_lut_x = make_edge_detection_lut(2)
edge_lut_y = make_edge_detection_lut(0)
edge_lut_z = make_edge_detection_lut(1)

def evaluate_lut(lut):
    img = generate_image(lut)
    img_valid = img[filter_steps:-filter_steps, filter_steps:-filter_steps]

    edge_pixels = (img_valid.shape[0] - 2) * (img_valid.shape[1] - 2)
    edge_count_x = lut2d.binary_lut_filter(img_valid, edge_lut_x).astype('f').sum() / edge_pixels
    edge_count_y = lut2d.binary_lut_filter(img_valid, edge_lut_y).astype('f').sum() / edge_pixels
    edge_count_z = lut2d.binary_lut_filter(img_valid, edge_lut_z).astype('f').sum() / edge_pixels

    loss_edges = 0
    loss_edges += (edge_count_x - target_edge_count)**2
    loss_edges += (edge_count_y - target_edge_count)**2
    loss_edges += (edge_count_z - target_edge_count)**2
    loss_brightness = 100 * (np.mean(img_valid) - target_brigthness) ** 2
    # print('loss_edges:', loss_edges)
    # print('loss_brightness:', loss_brightness)
    return loss_edges + loss_brightness

def main():
    iterations = 100
    best_factor = 0.01
    population_size = 10000

    # probability distribution over all (512-bit --> 1-bit) look-up tables
    #
    # (We don't track any dependencies/correlations; it's simply the
    #  probability that each of the 512 inputs gives a True output.)
    #
    probs = np.ones(2**7) * 0.5

    for it in range(iterations):
        print('iteration', it)

        population = []
        for j in range(population_size):
            lut = (np.random.random(probs.shape) < probs).astype('uint8')
            loss = evaluate_lut(lut)
            population.append((loss, lut))

        population.sort(key=lambda x: x[0])
        losses = np.array([ind[0] for ind in population])
        luts = np.array([ind[1] for ind in population])

        print('best loss: %.6f' % losses[0])
        print('mean loss: %.6f' % losses.mean())

        # save to disk
        with open('best-lut-it%05d.txt' % it, 'w') as f:
            np.savetxt(f, luts[0])
        img = generate_image(luts[0]).astype('uint8')
        t0 = time.time()
        # imageio.imwrite('best-lut-it%05d.png' % it, img * 255, compress_level=6)
        render.render(img, 'best-lut-it%05d.png' % it)
        print(f'render took {time.time() - t0} seconds')

        # estimate the new probability distribution from the best samples
        probs = luts[:int(population_size * best_factor), :].mean(0)
        print('some probs are', probs[:8])
        # probs = probs.clip(0.003, 0.997)  # add a minimum amount of noise

        def binary_entropy(x):
            return -(sc.xlogy(x, x) + sc.xlog1py(1 - x, -x)) / np.log(2)
        print('entropy is %.6f bits' % binary_entropy(probs).sum())


if __name__ == '__main__':
    main()
