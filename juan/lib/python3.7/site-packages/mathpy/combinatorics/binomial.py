# encoding=utf8


"""
Module containing methods related to computing binomial coefficients.

"""

from decimal import Decimal, localcontext

import numpy as np

from mathpy.combinatorics.factorial import factorial


def binom_coeff(n, k, method=None):
    r"""
    Interface function to the BinomialCoefficient class which contains several methods for
    computing the binomial coefficient :math:`\binom{n}{k}`.

    Parameters
    ----------
    n : int
        Number of possibilities
    k : int
        number of unordered outcomes
    method : {'recursive', 'multiplicative', 'factorial'}, optional
        Sets method to calculate binomial coefficient. Defaults to multiplicative. Be warned
        the recursive method for larger integers can take an exorbitant amount of time to
        complete.

    Returns
    -------
    bico : float
        The binomial coefficient.

    Notes
    -----
    The binomial coefficient :math:`\binom{n}{k}` is defined as the number of ways of selecting a
    set of :math:`k` elements (unordered) from a set of :math:`n` elements and is read as
    :math:`n` choose :math:`k`. The compact form of the binomial coefficient equation is defined as:

    .. math::

        \binom{n}{k} = \frac{n!}{k!(n - k)!} \qquad 0 \leq k \leq n

    Examples
    --------
    >>> binom_coeff(4, 2)
    6
    >>> binom_coeff(10, 5)
    252
    >>> binom_coeff(50, 25, 'multiplicative')
    126410606437752.0
    >>> binom_coeff(50, 25, 'factorial')
    126410606437752.02
    >>> binom_coeff(100, 50)
    1.0089134454556422e+29
    >>> binom_coeff(100, 50, 'factorial')
    1.0089134454556424e+29

    References
    ----------
    Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
        Cambridge: Cambridge University Press.

    Weisstein, Eric W. "Binomial Coefficient." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/BinomialCoefficient.html

    """
    binom_method = {
        'recursive': 'binomial_recursive',
        'multiplicative': 'binomial_multiplicative',
        'factorial': 'binomial_factorial'
    }
    if k == 0:
        return 1.0

    x = BinomialCoefficient(n, k)

    try:
        if method is None:
            f = getattr(x, x.method)
        elif hasattr(x, binom_method[method]):
            f = getattr(x, binom_method[method])

    except KeyError:
        print('no attribute with name ' + str(method))
        raise

    if method == 'binomial_recursive' or method == 'recursive' \
            or x.method == 'binomial_recursive' or x.method == 'recursive':
        return f(n, k)
    else:
        return f()


class BinomialCoefficient(object):
    r"""
    Class containing different algorithmic implementations of calculating the binomial coefficient.

    Attributes
    ----------
    method : string
        Sets the default binomial coefficient calculation method.

    Methods
    -------
    binomial_recursive()
        Implements a recursive scheme to calculate the binomial coefficient.
    binomial_multiplicative()
        Computes the binomial coefficient using a multiplicative formula.
    binomial_factorial()
        Computes the binomial coefficient using the compact form. Computationally
        unstable for larger values of :math:`n` and :math:`k` and thus other
        approaches are preferred; however, it is presented here for completeness.

    Notes
    -----
    The binomial coefficient :math:`\binom{n}{k}` is defined as the number of ways of selecting a
    set of :math:`k` elements (unordered) from a set of :math:`n` elements and is read as
    :math:`n` choose :math:`k`. The compact form of the binomial coefficient equation is defined as:

    .. math::

        \binom{n}{k} = \frac{n!}{k!(n - k)!} \qquad 0 \leq k \leq n

    See Also
    --------
    Specific method implementations for more details on algorithms.

    References
    ----------
    Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
        Cambridge: Cambridge University Press.

    Weisstein, Eric W. "Binomial Coefficient." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/BinomialCoefficient.html

    """
    def __init__(self, n, k):
        if k < 0 or n <= 0 or k > n:
            raise ValueError('Incorrect arguments to compute binomial coefficient')

        self.n = n
        self.k = k
        self.method = 'binomial_multiplicative'

    def binomial_recursive(self, n, k):
        r"""
        Computes the binomial coefficient :math:`\binom{n}{k}` by a recursive approach.
        The recursion approach is generally recommended due to its computational stability
        compared to other methods.

        Parameters
        ----------
        n : int
            Number of possibilities
        k : int
            number of unordered outcomes

        Returns
        -------
        float
            The binomial coefficient

        Notes
        -----
        The recursive method of the binomial coefficient calculation is defined as:

        .. math::

            \binom{n}{k} = \binom{n - 1}{n - k} + binom{n - 1}{k} \qquad for n, k: 1 \leq k \leq n - 1

        With boundary values:

        .. math::

            \binom{n}{0} = \binom{n}{n} = 1

        References
        ----------
        Binomial coefficient. (2017, April 17). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Binomial_coefficient&oldid=775905810

        Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
            Cambridge: Cambridge University Press.

        Weisstein, Eric W. "Binomial Coefficient." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BinomialCoefficient.html

        """
        if k == n or k == 0:
            return 1
        else:
            return self.binomial_recursive(n-1, k-1) + self.binomial_recursive(n-1, k)

    def binomial_multiplicative(self):
        r"""
        Implementation of the binomial coefficient computation with the multiplicative equation.

        Parameters
        ----------
        n : int
            Number of possibilities
        k : int
            number of unordered outcomes

        Returns
        -------
        float
            The binomial coefficient

        Notes
        -----
        The multiplicative method for computing the binomial coefficient is more efficient than
        the compact form calculation and is defined as:

        .. math::

            \binom{n}{k} = \frac{n(n-1)(n-2) \cdots (n-(k-1))}{k(k-1)(k-2) \cdots 1} = \prod^k_{i=1} \frac{n + 1 - i}{i}

        References
        ----------
        Binomial coefficient. (2017, April 17). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Binomial_coefficient&oldid=775905810

        Binomial coefficients. Encyclopedia of Mathematics.
            From http://www.encyclopediaofmath.org/index.php?title=Binomial_coefficients&oldid=39155

        Weisstein, Eric W. "Binomial Coefficient." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BinomialCoefficient.html

        """
        bico = 1
        nk = np.minimum(self.n, self.n - self.k)
        j = 1
        for _ in np.arange(nk):
            bico *= (float(self.n + 1 - j) / float(j))
            j += 1

        return bico

    def binomial_factorial(self):
        r"""
        Implementation of the binomial coefficient computation. Not meant for actual computation
        as the other methods available are more efficient.

        Parameters
        ----------
        n : int
            Number of possibilities
        k : int
            number of unordered outcomes

        Returns
        -------
        float
            The binomial coefficient

        Notes
        -----
        The binomial coefficient equation (in compact form) is defined as:

        .. math::

            \binom{n}{k} = \frac{n!}{k!(n-k)!} \qquad 0 \leq k \leq n

        References
        ----------
        Binomial coefficient. (2017, April 17). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Binomial_coefficient&oldid=775905810

        Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
            Cambridge: Cambridge University Press.

        Weisstein, Eric W. "Binomial Coefficient." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BinomialCoefficient.html

        """
        nk = np.minimum(self.n, self.n - self.k)

        if nk >= 100:
            with localcontext() as ctx:
                ctx.prec = 50
                bico = Decimal(factorial(self.n)) / (Decimal(factorial(self.k)) * Decimal(factorial(nk)))
        else:
            bico = float(factorial(self.n)) / float(factorial(self.k) * factorial(nk))

        return bico
