# encoding=utf8


"""
Module containing functions and methods related to primes and some elementary number theory.

"""


import numpy as np
from mathpy.numtheory.gcd import gcd


def isprime(n):
    r"""
    Tests whether a given integer :math:`n` is prime.

    Parameters
    ----------
    n : int, float
        Value to test

    Returns
    -------
    Boolean
        Returns True if :math:`n` is prime, False otherwise.

    Examples
    --------
    >>> isprime(9)
    False
    >>> isprime(3)
    True

    Notes
    -----
    A prime number is defined as a positive integer, :math:`n > 1` that
    has no positive divisors other than 1 and itself.

    References
    ----------
    Weisstein, Eric W. "Prime Number." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/PrimeNumber.html

    """
    if n != np.round(n):
        return False

    if n == 1:
        return False
    elif n == 2 or n == 3:
        return True

    if n % 2.0 == 0 or n % 3.0 == 0:
        return False

    for i in np.arange(5, np.floor(np.sqrt(n))):
        if n % float(i) == 0 or n % float(i + 2) == 0:
            return False

    return True


def isrelativelyprime(a, b):
    r"""
    Tests if two integers are relatively prime.

    Parameters
    ----------
    a : int

    b : int

    Returns
    -------
    Boolean
        Returns True if :math:`a` and :math:`b` are relatively prime, False otherwise.

    Notes
    -----
    Two integers :math:`a` and :math:`b` are said to be relatively prime (also called
    coprime or co-prime) if they share no positive divisors except 1.

    References
    ----------
    Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms
        (3rd ed., pp. 931). Cambridge (Inglaterra): Mit Press.

    Weisstein, Eric W. "Relatively Prime." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/RelativelyPrime.html

    """
    if gcd(a, b) == 1:
        return True

    return False


def iscomposite(n):
    r"""
    Tests whether a given value :math:`n` is composite. Essentially the opposite
    of the isprime() function

    Parameters
    ----------
    n : int, float
        Value to test

    Returns
    -------
    Boolean
        Returns True if :math:`n` is composite, False otherwise.

    Examples
    --------
    >>> iscomposite(9)
    True
    >>> iscomposite(3)
    False

    Notes
    -----
    A composite number is defined as a positive integer :math:`n` that has a factorinteger
    than 1 and itself. In short, a composite number is not prime.

    References
    ----------
    Weisstein, Eric W. "Composite Number." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/CompositeNumber.html

    """
    if isprime(n) is True:
        return False
    else:
        return True


def isodd(n):
    r"""
    Simple function to test whether a given value is odd.

    Parameters
    ----------
    n : int, float
        Value to test

    Returns
    -------
    Boolean
        Returns True if :math:`n` is odd, False otherwise.

    Examples
    --------
    >>> isodd(5)
    True
    >>> isodd(4)
    False
    >>> isodd(5.25)
    False

    Notes
    -----
    An odd number is an integer that has the form :math:`n = 2k + 1` for an integer
    :math:`k`. In other words, an odd number is an integer that is not evenly
    divisible by 2.

    References
    ----------
    Weisstein, Eric W. "Odd Number." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/OddNumber.html

    """
    if n != np.round(n):
        return False

    if n % 2.0 == 0:
        return False

    return True


def iseven(n):
    r"""
    Simple function to test whether a given value is even.

    Parameters
    ----------
    n : int, float
        Value to test

    Returns
    -------
    Boolean
        Returns True if :math:`n` is even, False otherwise.

    Examples
    --------
    >>> iseven(5)
    False
    >>> iseven(4)
    True
    >>> iseven(4.23)
    False

    Notes
    -----
    An even number is defined as an integer with the form :math:`n = 2k` where :math:`k`
    is also an integer. Put differently, an even number is not odd and is thus evenly
    divisible by 2.

    References
    ----------
    Weisstein, Eric W. "Even Number." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/EvenNumber.html

    """
    if n != np.round(n):
        return False

    if isodd(n) is True:
        return False

    return True


def issquare(n):
    r"""
    Tests if a given integer is a square number.

    Parameters
    ----------
    n : int
        Integer to test

    Returns
    -------
    Boolean
        True if n is a square number, False otherwise

    Examples
    --------
    >>> issquare(25)
    True
    >>> issquare(8)
    False

    References
    ----------
    Barnes, C. (2004). Integer Factorization Algorithms (1st ed.).
            Corvallis, OR: Department of Physics, Oregon State University.

    """
    if np.power(np.ceil(np.sqrt(n)), 2) == np.ceil(n):
        return True

    return False
