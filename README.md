# lut2d-search

This is a quick experiment to learn a small (3x3) 2D filter for binary images.

![example output images](example-results/example-results.png?raw=true)

The goal is to discover a filter that can generate maze-like blob structures when applied multiple times over white noise. There are 2^512 possible 3x3 filters, too many for an exhaustive search.

This is a simple use-case for the [Cross-Entropy method](https://en.wikipedia.org/wiki/Cross-Entropy_Method). We sample 10'000 filters from a probability distribution and evaluate them. The best 100 (one percent) are used to estimate the next distribution from scratch.

In contrast to other methods (evolution strategies), the remaining 99 percent are discarded and no statistics are tracked. In contrast to genetic algorithms we are tracking a distribution, not individuals.
