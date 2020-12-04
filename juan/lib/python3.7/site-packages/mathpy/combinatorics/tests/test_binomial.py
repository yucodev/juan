import numpy as np
import pytest

from mathpy.combinatorics.binomial import binom_coeff


def test_binomial_recursive():
    n = (1, 3, 5, 10)
    k = (1, 2, 3, 5)
    expected = (1, 3, 10, 252)

    for i in np.arange(len(n)):
        np.testing.assert_almost_equal(binom_coeff(n[i], k[i], 'recursive'), expected[i])

    np.testing.assert_equal(binom_coeff(3, 0), 1)
    np.testing.assert_equal(binom_coeff(3, 3), 1)


def test_binomial_multi():
    n = (1, 3, 5, 10, 20, 50, 100, 200)
    k = (1, 2, 3, 5, 10, 30, 50, 100)
    expected = (1, 3, 10, 252, 184756, 47129212243960, 100891344545564193334812497256,
                90548514656103281165404177077484163874504589675413336841320)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(binom_coeff(n[i], k[i], 'multiplicative'), expected[i])


def test_binomial_factorial():
    n = (1, 3, 5, 10, 20, 50, 100, 200)
    k = (1, 2, 3, 5, 10, 30, 50, 100)
    expected = (1, 3, 10, 252, 184756, 47129212243960, 100891344545564193334812497256,
                90548514656103281165404177077484163874504589675413336841320)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(binom_coeff(n[i], k[i], 'factorial'), expected[i])


def test_binomial_raises():
    with pytest.raises(KeyError):
        binom_coeff(5, 3, 'NA_METHOD')


def test_binomial_args():
    with pytest.raises(ValueError):
        binom_coeff(2, 3)
    with pytest.raises(ValueError):
        binom_coeff(2, -3)
