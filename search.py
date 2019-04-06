#!/usr/bin/env python3
import numpy as np
import scipy.special as sc
import lut2d
import imageio

size = 64
target_edge_count = 9
target_brigthness = 0.4
filter_steps = 13

def generate_image(lut, count=filter_steps):
    # generate binary noise image
    img = np.random.randint(0, 2, (size, size), dtype='uint8')
    # apply the lut as filter several times
    for j in range(count):
        img = lut2d.binary_lut_filter(img, lut)
    return img

def evaluate_lut(lut):
    img = generate_image(lut)
    edge_counts_y = np.sum(np.diff(img, axis=0) != 0, axis=0)
    edge_counts_x = np.sum(np.diff(img, axis=1) != 0, axis=1)
    loss_y = np.mean((edge_counts_y.astype('float') - target_edge_count)**2)
    loss_x = np.mean((edge_counts_x.astype('float') - target_edge_count)**2)
    loss_brightness = 1000 * (np.mean(img) - target_brigthness) ** 2
    return loss_y + loss_x + loss_brightness

def main():
    iterations = 100
    best_factor = 0.01
    population_size = 10000

    # probability distribution over all (512-bit --> 1-bit) look-up tables
    #
    # (We don't track any dependencies/correlations; it's simply the
    #  probability that each of the 512 inputs gives a True output.)
    #
    probs = np.ones(2**9) * 0.5

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
        print('mean loss was', losses.mean())

        # save to disk
        with open('best-lut-it%05d.txt' % it, 'w') as f:
            np.savetxt(f, luts[0])
        img = generate_image(luts[0]).astype('uint8')
        img[img != 0] = 255
        imageio.imwrite('best-lut-it%05d.png' % it, img, compress_level=6)

        # estimate the new probability distribution from the best samples
        probs = luts[:int(population_size * best_factor), :].mean(0)
        print('some probs are', probs[:8])
        # probs = probs.clip(0.003, 0.997)  # add a minimum amount of noise

        def binary_entropy(x):
            return -(sc.xlogy(x, x) + sc.xlog1py(1 - x, -x)) / np.log(2)
        print('entropy is %.6f bits' % binary_entropy(probs).sum())


if __name__ == '__main__':
    main()
