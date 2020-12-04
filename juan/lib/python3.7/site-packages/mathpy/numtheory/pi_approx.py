import numpy as np

from mathpy.combinatorics.binomial import binom_coeff


def ramanujan_approx(verbose=False):
    s = 0.0
    n = 1

    while s != (1 / np.pi):
        s += float(binom_coeff(2.0 * n, n) ** 3.0 * ((42.0 * n + 5.0) / (2.0 ** (12.0 * n + 4.0))))
        n += 1.0

        if verbose is True:
            print(s, n)

    return s
