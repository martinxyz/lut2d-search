# lut2d-search

This is a quick experiment to learn a small (3x3) 2D filter for binary images. The goal is to discover a filter that can generate a nice maze-like blob pattern.

![example output images](docu/example-results.png?raw=true)

To generate this pattern, the filter is first applied over a 64x64 white noise image. On the output the filter is applied again. This is repeated 13 times to produce the final output.

The filter is a generic 3x3 look-up table (9 bits input, 1 bit output):

![3x3 look-up table filter](docu/3x3-filter-lut.png?raw=true)

There are 2^512 possible 3x3 filters, too many for exhaustive search. Also, the process is highly non-linear. In fact, one of those filters is [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). Flipping a single bit can completely change the output patterns.

This is a good use-case for the [Cross-Entropy method](https://en.wikipedia.org/wiki/Cross-Entropy_Method):

1. Sample 10'000 random filters from a probability distribution.
2. Evaluate them using a loss function.
3. Use the best 1% to estimate the next distribution from scratch.
4. Repeat.

### Details

The loss function is the distance to a target brightness and edge count. When you execute the code, note that getting a nice pattern requires a bit of luck. About 50% of the runs generate small ugly triangles instead.

The probability distribution is one value for each bit of the look-up table, tracking the probability that this bit should be one. Dependencies and correlations between the bits exist but are not modeled.

### Extra Results

I have also tried novelty search to evolve 42 rules simultanously with the goal of maximizing diversity. To measure diversity, the first few layers of a pre-trained ResNet50 was used to create a "behaviour descriptor". You can browse [some results from that run](https://log2.ch/diversity-lut-search/), but code is not published yet, also, it's a hacky mess.
