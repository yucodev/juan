# encoding=utf8


import numpy as np


def bernoulli(p=0.5, size=1):
    r"""
    Generates random samples from the Bernoulli distribution.

    Parameters
    ----------
    p : probability of success, default 0.5
        The probability of success of a Bernoulli trial (Yes/No, Pass/Fail, etc.). Must be between
        0 and 1
    size : int, default 1
        The number of random Bernoulli samples to generate.

    Returns
    -------
    list or boolean
        List containing the generated Bernoulli random samples represented by boolean True/False values.
        If size is 1, the single generated sample is returned as a boolean.

    Notes
    -----

    See Also
    --------
    Bernoulli : class
        Class containing several methods related to estimating Bernoulli random variates.

    References
    ----------


    """
    if 0.0 > p or p > 1.0:
        raise ValueError('p must be between 0 and 1')
    if size < 1:
        raise ValueError('size parameter must be at least 1')
    if np.floor(size) != size:
        size = np.floor(size)

    b = []
    for _ in np.arange(size):
        b.append(continuous_uniform() < p)

    if len(b) == 1:
        b = b[0]

    return b


def binomial(n=5, p=0.5, size=1):
    if 0.0 > p or p > 1.0:
        raise ValueError('p must be between 0 and 1')
    if n < 0:
        raise ValueError('n must be at least 0')
    if np.floor(n) != n:
        n = np.floor(n)
    if size < 1:
        raise ValueError('size parameter must be at least 1')
    if np.floor(size) != size:
        size = np.floor(size)

    bi = []

    for _ in np.arange(size):
        s = 0

        for _ in np.arange(n):
            s += bernoulli(p)

        bi.append(s)

    if len(bi) == 1:
        bi = bi[0]

    return bi


def continuous_uniform(a=0.0, b=1.0, size=1):
    if a > b:
        raise ValueError('parameter b must be greater than a')
    if size < 1:
        raise ValueError('size parameter must be at least 1')
    if np.floor(size) != size:
        size = np.floor(size)

    u = []
    for _ in np.arange(size):
        u.append(a + (b - a) * np.random.random_sample())

    if len(u) == 1:
        u = u[0]

    return u


# def hypergeometric(n, N, K):
#     if n < 1:
#         raise ValueError('number of trials must be at least 1')
#     elif n > N:
#         raise ValueError('number of trials must be higher than population of elements')
#     elif N < 1:
#         raise ValueError('population of elements must be at least 1')
#     elif K < 0:
#         raise ValueError('number of successes must be at least 0')
#
#     h = 0
#
#     for _ in np.arange(n):
#         p = K / N
#
#         if bernoulli(p):
#             h += 1
