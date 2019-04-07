# lut2d-search

This is a quick experiment to learn a small (3x3) 2D filter for binary images. The goal is to discover a filter that can generate a nice maze-like blob pattern.

![example output images](docu/example-results.png?raw=true)

To generate this pattern, the filter is first applied over a 64x64 whilte noise image. On the output image, the same filter is applied again. This process is repeated 13 times to produce the final output.

The filter is a generic 3x3 look-up table (9 bits input, 1 bit output):

![3x3 look-up table filter](docu/3x3-filter-lut.svg?raw=true)

There are 2^512 possible 3x3 filters, too many for an exhaustive search. The whole process is highly non-linear. One of those filters is in fact the rule for [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), which is touring-complete. Flipping a single bit can result in completely different output patterns.

This is a good use-case for the [Cross-Entropy method](https://en.wikipedia.org/wiki/Cross-Entropy_Method):

1. Sample 10'000 random filters from a probability distribution.
2. Evaluate them using a loss function.
3. Use the best 100 samples (1%) to estimate a new distribution from scratch.
4. Repeat.

In contrast to other methods (evolution strategies), the remaining 99 percent are discarded and no statistics are tracked. In contrast to genetic algorithms we are tracking a distribution, not individuals.

As loss function, a target value for the edge count and for the average brightness is used. Using edge count alone results in tiny well-spaced dots, which is not so interesting.

The new distribution should be as similar as possible to the distribution of the best one percent. The [cross entropy](https://en.wikipedia.org/wiki/Cross_entropy) can be used as a measure this similarity. We model our distribution as a probability for each bit of the look-up table to be one. (No dependencies or correlations are not modelled.) This distribution is very simple to estimate from data. We can count how many of the best filters have a certain bit set, and use the fraction as the new probability for this bit.
