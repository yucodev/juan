# encoding=utf8


import numpy as np


def gcd(a, b, method=None):
    r"""
    Calculates the greatest common divisor of two integers using the Euclidean
    algorithm. Methods for computing the GCD are called from the GCD class.
    Both :math:`a` and :math:`b` cannot be 0. Please see the GCD class for
    more documentation on the specific methods and their respective implementations.

    Parameters
    ----------
    a : int or float

    b : int or float

    method: {None, 'gcd_recursive', 'gcd_division', gcd_subtraction'}, optional
        Specifies the algorithm used to compute the GCD. Defaults to the recursive
        algorithm.

    Returns
    -------
    gcd : integer
        The greatest common divisor of :math:`a` and :math:`b`

    Examples
    --------
    >>> gcd(12, 8)
    4
    >>> gcd(24, 30)
    6
    >>> gcd(9, 5)
    1
    >>> gcd(14.0, 21.0)
    7.0

    """
    x = _GCD(a, b)
    if method is None:
        f = getattr(x, x.method)
        return f(a, b)
    else:
        if hasattr(x, method):
            f = getattr(x, method)
            if method == 'recursive':
                return f(a, b)
        else:
            raise ValueError('no method with name ' + str(method))

    return f()


class _GCD(object):
    r"""
    Class containing several different implementations of the Euclidean
    algorithm for computing the greatest common divisor of two integers,
    :math:`a` and :math:`b`. Please see the specific methods for further
    documentation on their respective approaches and implementations.

    Attributes
    ----------
    a : int

    b : int

    method : {'gcd_recursive', 'gcd_division', 'gcd_subtraction'}, optional
        Specifies the algorithm used to compute the GCD.

    Methods
    -------
    gcd_recursive(a, b)
        Performs the recursive Euclidean algorithm for computing the GCD.
        Due to the method's recursive nature, parameters a and b must be
        specified.
    gcd_subtraction()
        Computes the GCD using Euclid's original version of the algorithm.
    gcd_division()
        Utilizes Euclidean division to calculate the gcd of two integers.

    Notes
    -----
    The greatest common divisor of two integers :math:`a` and :math:`b` is as
    it sounds. It is the greatest of the common divisors between two integers,
    for example :math:`gcd(32, 24) = 8`. The following are some properties of
    the greatest common divisor algorithm.

    - :math:`gcd(a, b) = gcd(b, a)`
    - :math:`gcd(a, b) = gcd(-a, b)`
    - :math:`gcd(a, b) = gcd(|a|, |b|)`
    - :math:`gcd(a, 0) = |a|`
    - :math:`gcd(a, ka) = |a|` for any integer :math:`k`.

    References
    ----------
    Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms (3rd ed., pp. 928-930).
        Cambridge (Inglaterra): Mit Press.

    """
    def __init__(self, a, b):
        if a == 0 and b == 0:
            raise ValueError('a and b cannot both be 0.')
        self.a = np.absolute(a)
        self.b = np.absolute(b)
        self.method = 'recursive'

    def division(self):
        r"""
        Computes the greatest common divisor of two integers, :math:`a` and :math`b`,
        utilizing Euclidean division.

        Returns
        -------
        gcd : int
            The greatest common divisor of :math:`a` and :math`b`.

        Notes
        -----
        The Euclidean division implementation of the greatest common divisor algorithm computes a
        quotient :math:`q_k` and a remainder :math:`r_k` at each step :math:`k` from the two numbers
        :math:`a` and :math:`b`. The quotient component of Euclidean division is not used in the
        algorithm, thus only modulo operations are required as that only returns the remainder.

        References
        ----------
        Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms (3rd ed., pp. 928-930).
            Cambridge (Inglaterra): Mit Press.

        Euclidean algorithm. (2017, May 18). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Euclidean_algorithm&oldid=780973502

        Euclidean division. (2017, May 10). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Euclidean_division&oldid=779699188

        """
        while self.b != 0:
            x = self.b
            self.b = self.a % self.b
            self.a = x

        return self.a

    def subtraction(self):
        r"""
        Computes the greatest common divisor using the original implementation of the algorithm by
        Euclid. In this version of the algorithm, the quotient :math:`q_k` and remainder :math:`r_k`
        is calculated by repeated division by subtraction. Therefore, in this implementation of the
        greatest common divisor algorithm, the modulo operation in the division implementation is
        replaced by division by repeated subtraction.

        Returns
        -------
        gcd : int or float
            The greatest common divisor of :math:`a` and :math`b`.

        References
        ----------
        Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms (3rd ed., pp. 928-930).
            Cambridge (Inglaterra): Mit Press.

        Euclidean algorithm. (2017, May 18). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Euclidean_algorithm&oldid=780973502

        """
        while self.a != self.b:

            if self.a > self.b:
                self.a -= self.b
            else:
                self.b -= self.a

        return self.a

    def recursive(self, a, b):
        r"""
        Implements a recursive version of the greatest common divisor algorithm.

        Parameters
        ----------
        a : int or float

        b : int or float

        Notes
        -----
        The recursive implementation of the greatest common divisor algorithm
        was described in the Elements of Euclid but may even predate that.

        Returns
        -------
        gcd : int
            The greatest common divisor of :math:`a` and :math`b`.

        References
        ----------
        Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms
            (3rd ed., pp. 928-930, 934-935). Cambridge (Inglaterra): Mit Press.

        Euclidean algorithm. (2017, May 18). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Euclidean_algorithm&oldid=780973502

        """

        if b == 0:
            return a
        else:
            return self.recursive(b, a % b)


def gcd_extended(a, b):
    r"""
    Implements the extended form of the Euclidean algorithm which computes the greatest common
    divisor :math:`d` and integers :math:`x` and :math:`y` such that :math:`ax + by = d` as
    stated by Bezout's identity.

    Parameters
    ----------
    a : int or float

    b : int or float

    Returns
    -------
    tuple
        Returns tuple containing the greatest common divisor :math:`d`, and integers :math:`x`
        and :math:`y`, respectively.

    Notes
    -----
    The extended Euclidean algorithm computes the greatest common divisor, :math:`d` of two
    integers :math:`a` and :math:`b` as well as the coefficients :math:`x` and :math:`y` such
    that:

    .. math::

        d = gcd(a, b) = ax + by

    The coefficients :math:`x` and :math:`y` are known as Bezout's coefficients and can be zero
    or negative.

    Examples
    --------
    >>> gcd_extended(99, 78)
    (3, -11, 14)
    >>> 99 * -11 + 78 * 14
    3

    References
    ----------
    Bezout's identity. (2017, May 12). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=B%C3%A9zout%27s_identity&oldid=780050687

    Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms
        (3rd ed., pp. 937-938). Cambridge (Inglaterra): Mit Press.

    """
    if a == 0 and b == 0:
            raise ValueError('a and b cannot both be 0.')

    if b == 0:
        return (a, 1, 0)
    else:
        (d, x, y) = gcd_extended(b, a % b)
        (d, x, y) = (d, y, x - (a // b) * y)

        return (d, x, y)
