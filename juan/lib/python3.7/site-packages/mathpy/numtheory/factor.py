# encoding=utf8

"""
Methods for factoring integers into products of smaller primes.

"""

import numpy as np
from mathpy.numtheory.integers import issquare, isprime
from mathpy.numtheory.gcd import gcd


def factor_trial(n):
    r"""
    Front-end function for performing integer factorization.

    Parameters
    ----------
    n : int or float
        Integer to be factored into product of smaller integers.

    Returns
    -------
    tuple
        A list containing the factors of :math:`n` should they exist. If :math:`n`
        is prime, the returned list will only contain :math:`n`.

    Examples
    --------
    >>> factor_trial(4)
    [2.0, 2.0]
    >>> factor_trial(13)
    13
    >>> n = 9.24
    >>> factor_trial(n)
    [3.0, 3.0]

    Notes
    -----
    Integer factorization by trial division is the most inefficient algorithm for decomposing
    a composite number. Trial division is the method of testing if :math:`n` is divisible by
    a smaller number, beginning with 2 and proceeding upwards. This order is used to eliminate
    the need to test for multiples of 2 and 3. Also, the trial factors never need to go further
    than the square root of :math:`n`, :math:`\sqrt{n}`, due to the fact that if :math:`n` has
    a factor, there exists a factor :math:`f \leq \sqrt{n}`.

    References
    ----------
    Trial division. (2017, April 30). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Trial_division&oldid=778023614

    """
    if n != np.floor(n):
        n = np.floor(n)
    if isprime(n) or np.absolute(n) < 2:
        return [1, n]

    div = 2.0
    factors = []

    while n % div == 0:
        factors.append(div)
        n /= div

    div += 1

    while n > 1 and div <= np.sqrt(n):
        if n % div == 0:
            factors.append(div)
            n /= div
        else:
            div += 2

    if n > 1:
        factors.append(n)

    return factors


def fermat(n):
    r"""
    Computes the factorization of an integer :math:`n` by Fermat's factorization method.

    Parameters
    ----------
    n : int or float
        Integer to compute the factorization using Fermat's approach. If the supplied value
        is not an integer, the function coerces the value into an integer.

    Returns
    -------
    tuple
        Contains the factors of :math:`n`, :math:`a` and :math:`b` defined by
        Fermat's factorization theorem.

    Notes
    -----
    Fermat's factorization theorem redefines a composite number :math:`n` as the
    difference of squares:

    .. math::

        n = a^2 - b^2

    Which can also be written as:

    .. math::

            n = (a + b)(a - b)

    Examples
    --------
    >>> fermat(5959)
    (59, 101)

    References
    ----------
    Barnes, C. (2004). Integer Factorization Algorithms (1st ed.).
        Corvallis, OR: Department of Physics, Oregon State University.

    Fermat's factorization method. (2017, January 31). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Fermat%27s_factorization_method&oldid=763010603

    """
    if n != np.floor(n):
        n = np.floor(n)
    if isprime(n) or np.absolute(n) < 2:
        return 1, n

    a = np.ceil(np.sqrt(n))
    b = np.power(a, 2) - n
    while issquare(np.sqrt(b)) is False:
        a += 1
        b = np.power(a, 2) - n

    return a, np.sqrt(b)


def pollardrho(n):
    r"""
    Implementation of Pollard's rho algorithm for factorizing an integer :math:`n`
    into two non-trivial prime numbers.

    Returns
    -------
    tuple
        List containing the two prime factors of :math:`n`, should they exist.

    Notes
    -----
    Pollard rho Factorization is another algorithm for factoring an integer :math:`n` where
    :math:`n = pq`. :math:`n` . Pollard's rho factorization iterates the formula:

    .. math::

        x_{n+1} = x_n^2 + a(mod n)

    The algorithm is much more efficient than the trial division factorization method but can
    be very slow under poor conditions.

    Examples
    --------
    >>> pollardrho(8051)
    (97, 83)
    >>> pollardrho(10403)
    (101, 103)

    References
    ----------
    Barnes, C. (2004). Integer Factorization Algorithms (1st ed.).
        Corvallis, OR: Department of Physics, Oregon State University.

    Pollard's rho algorithm. (2017, May 6). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Pollard%27s_rho_algorithm&oldid=779076841

    Weisstein, Eric W. "Pollard rho Factorization Method." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/PollardRhoFactorizationMethod.html

    """
    if n != np.floor(n):
        n = np.floor(n)
    if isprime(n) or np.absolute(n) < 2:
        return 1, n

    x = 2
    y = 2
    d = 1

    while d == 1:
        x = (np.power(x, 2) + 1) % n
        y = (np.power(np.power(y, 2) + 1, 2) + 1) % n
        d = gcd(np.absolute(x - y), n)

    if d == n:
        return 'Could not find factor'
    else:
        return d, n // d
