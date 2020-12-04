# encoding=utf8


"""
Module containing functions for evaluating and interpolating polynomials.

"""

import numpy as np
from sympy import Symbol, Poly, simplify
from sympy.parsing.sympy_parser import parse_expr

from mathpy._lib import _create_array


def horner_eval(f, x0):
    r"""
    Evaulates a polynomial function using Horner's method.

    Parameters
    ----------
    f : function
        The polynomial function to be evaluated. For example, to evaluate the
        polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, f should be similar to:

        .. code-block:: python

            def f(x):
                # The variable in function f must be set as x.
                return 3 * x^3 - 5 * x^2 + 2 * x - 1

    x0 : int, float
        The point at which to evaluate the function f.

    Returns
    -------
    poly_eval : int or float
        The evaluated polynomial function f at the given point x0.

    Notes
    -----
    Given a polynomial, such as:

    .. math [1]

        a_0 + a_1 x + a_2 x^2 + a_3 x^3 + \cdots + a_n x^n

    Horner's method evaluates the polynomial at a given point, such
    as :math:`x_0` by converting the polynomial into a 'nested'
    form by defining a new sequence. This is done by starting with the
    leading coefficient :math:`a_n`, multiplying it :math:`x` and adding
    the next coefficient. For example, using Horner's method to evaluate
    the polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, at :math:`x = 3`
    Horner's method proceeds as follows:

    .. math::

        b_3 = 3

    .. math::

        b_2 = 3x - 5 = 3(3) - 5 = 4

    .. math::

        b_1 = (4)x + 2 = (4)(3) + 2 = 14

    .. math::

        b_0 = (14)x - 1 = (14)(3) - 1 = 41

    Examples
    --------
    >>> def f(x): return 3 * x ** 3 - 5 * x ** 2 + 2 * x - 1
    >>> horner_eval(f, 3)
    41
    >>> def f2(x): return 4 * x ** 4 - 6 * x ** 3 + 3 * x - 5
    >>> horner_eval(f2, 10)
    34025

    References
    ----------
    Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009).
        Introduction to algorithms (3rd ed.). Cambridge (Inglaterra): Mit Press.

    Horner's method. (2017, April 12). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Horner%27s_method&oldid=775072621

    """
    if callable(f) is False:
        raise TypeError('f must be a function')

    x = Symbol('x')
    fx_coefs = Poly(f(x), x).all_coeffs()

    poly_eval = 0
    for i in fx_coefs:
        poly_eval = poly_eval * x0 + i

    return poly_eval


def lagrange_interpolate(x, y):
    r"""
    Interpolates a polynomial given a set of equal-length x and y values using
    Lagrangian interpolation.

    Parameters
    ----------
    x
        One-dimensional array of x values. Can be a pandas DataFrame or Series,
        list, dictionary (first key-value pair is used if there are more than one),
        or numpy array. Must be same length as y.
    y
        One-dimensional array of y values. Can be a pandas DataFrame or Series,
        list, dictionary (first key-value pair is used if there are more than one),
        or numpy array. Must be same length as y.

    Returns
    -------
    Symbolic representation of interpolating polynomial.

    Notes
    -----
    The Lagrangian method of polynomial interpolation uses Lagrangian polynomials
    to fit a polynomial to a given set of data points. The Lagrange interpolating
    polynomial is given by the following theorem:

    For a set of data points :math:`(x_0, y_0), (x_1, y_1), \cdots, (x_n, y_n)`
    with no duplicate $x$ and there exists a function $f$ which evaluates to these
    points, then there is a unique polynomial $P(x)$ with degree $\leq n$ also
    exists. The polynomial is given by:

    .. math::

        P(x) = f(x_o)L_{n,0}(x) + \cdots + f(x_n)L_{n,n}(x) = \sum^n_{k=0} f(x_k) L_{n,k}(x)

    Where each :math:`k` in :math:`k = 0, 1, \cdots, n` is:

    .. math::

        L_{n,k} = \frac{(x - x_0)(x - x_1) \cdots (x - x_{k-1})(x - x_{k+1})
        \cdots (x - x_n)}{(x_k - x_0)(x_k - x_1) \cdots (x_k - x_{k-1})(x_k - x_{k+1})
        \cdots (x_k - x_n)} = \underset{i \neq k}{\prod^n_{i=0}} \frac{(x - x_i)}{(x_k - x_i)}

    Examples
    --------
    >>> x, y = [0, 2, 3, 4], [7, 11, 28, 63]
    >>> lagrange_interpolate(x, y)
    x**3 - 2*x + 7

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Cheney, E. W., & Kincaid, D. (2013). Numerical mathematics and computing (6th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    """
    x, y = _create_array(x)[0], _create_array(y)[0]

    if len(x) != len(y):
        raise ValueError('x and y must be the same length to evaluate polynomial')

    l = []

    for i in np.arange(len(x)):
        num = 1
        denom = 1

        p = np.delete(x, i)

        for j in p:
            num = str(num) + '*' + '(' + 'x' + ' - ' + str(j) + ')'
            denom = str(denom) + '*' + '(' + str(x[i]) + ' - ' + str(j) + ')'

        l.append('(' + num + ')' + '/' + '(' + denom + ')')

    poly = 0

    for i in np.arange(len(l)):
        poly = str(poly) + '+' + str(y[i]) + '*' + str(l[i])

    return simplify(poly)


def neville(x, y, x0):
    r"""
    Evaluates an interpolated polynomial at a particular :math:`x` value given a set of
    :math:`x` and corresponding :math:`y` values.

    Parameters
    ----------
    x
        One-dimensional array of x values. Can be a pandas DataFrame or Series,
        list, dictionary (first key-value pair is used if there are more than one),
        or numpy array. Must be same length as y.
    y
        One-dimensional array of y values. Can be a pandas DataFrame or Series,
        list, dictionary (first key-value pair is used if there are more than one),
        or numpy array. Must be same length as y.
    x0
        Desired value at which to interpolate and approximate poynomial.

    Returns
    -------
    tuple
        Contains the approximated value of the interpolated polynomial evaluated at the point :math:`x` as float
        and a numpy array representing the iterated Neville table with intermediate values generated recursively.

    Notes
    -----
    Neville's method evaluates a polynomial that passes through a given set of :math:`x` and :math:`y` points
    for a particular :math:`x` value using the Newton polynomial form. Neville's method is similar to a
    now defunct procedure named Aitken's algorithm and is based on the divided differences recursion
    relation.

    It was stated before in a previous post on Lagrangian polynomial interpolation that there exists
    a Lagrange polynomial that passes through points :math:`y_1, y_2, \cdots, y_k` where each is a
    distinct integer and :math:`0 \leq y_i \leq n` at corresponding x values :math:`x_0, x_1, x_2, \cdots, x_n`.
    The :math:`k` points :math:`y_1, y_2, \cdots, y_k` are denoted :math:`P_{y_1, y_2, \cdots, y_k}(x)`.
    Neville's method can be stated as follows:

    Let a function :math:`f` be defined at points :math:`x_0, x_1, \cdots, x_k` where :math:`x_j` and
    :math:`x_i` are two distinct members. For each :math:`k`, there exists a Lagrange polynomial :math:`P`
    that interpolates the function :math:`f` at the :math:`k + 1` points :math:`x_0, x_1, \cdots, x_k`.
    The :math:`k`th Lagrange polynomial is defined as:

    .. math::

        P(x) = \frac{(x - x_j) P_{0,1,\cdots,j-1,j+1,\cdots,k}(x) - (x - x_i)
        P_{0,1,\cdots,i-1,i+1,\cdots,k}(x)}{(x_i - x_j)}

    The :math:`P_{0,1,\cdots,j-1,j+1,\cdots,k}` and :math:`P_{0,1,\cdots,i-1,i+1,\cdots,k}` are often
    denoted :math:`\hat{Q}` and :math:`Q`, respectively, for ease of notation.

    .. math::

        P(x) = \frac{(x - x_j) \hat{Q}(x) - (x - x_i) Q(x)}{(x_i - x_j)}

    Examples
    --------
    >>> x, y = [8.1, 8.3, 8.6, 8.7], [16.9446, 17.56492, 18.50515, 18.82091]
    >>> neville(x, y, 8.4)
    17.8770925

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Cheney, E. W., & Kincaid, D. (2013). Numerical mathematics and computing (6th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Neville's algorithm. (2016, January 2). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Neville%27s_algorithm&oldid=697870140

    """
    x, y = _create_array(x)[0], _create_array(y)[0]

    if len(x) != len(y):
        raise ValueError('x and y must be the same length to evaluate polynomial')

    n = len(x)

    q = np.zeros((n, n))
    q[:, 0] = y

    for i in np.arange(1, n):
        for j in np.arange(i, n):
            q[j, i] = ((x0 - x[j - i]) * q[j, i - 1] - (x0 - x[j]) * q[j - 1, i - 1]) / (x[j] - x[j - i])

    return float(q[n - 1, n - 1]), q


def divided_differences(x, y, x0=None):
    r"""
    Constructs an interpolating polynomial that passes through given x and y points using
    the divided differences method.

    Parameters
    ----------
    x
        One-dimensional array of x values. Can be a pandas DataFrame or Series,
        list, dictionary (first key-value pair is used if there are more than one),
        or numpy array. Must be same length as y.
    y
        One-dimensional array of y values. Can be a pandas DataFrame or Series,
        list, dictionary (first key-value pair is used if there are more than one),
        or numpy array. Must be same length as y.
    x0
        Optional. Desired value to interpolate poynomial and approximate.

    Returns
    -------
    dict
        dict object containing the following entries:
        Approximated value of the intepolated polynomial (if given)
        The interpolated polynomial
        Divided Differences Table

    Notes
    -----
    The divided differences method is a numerical procedure for interpolating a polynomial
    given a set of points. Unlike Neville's method, which is used to approximate the value
    of an interpolating polynomial at a given point, the divided differences method
    constructs the interpolating polynomial in Newton form.

    Assume that :math:`P_n(x)` is the :math:`nth` Lagrangian polynomial that corresponds with
    the function :math:`f` at a set of :math:`x` data points. The polynomial :math:`P_n(x)` can be expressed
    using the divided differences of the function :math:`f` with respect to the :math:`x`-values.

    .. math::

        P_n(x) = a_0 + a_1(x - x_0) + a_2(x - x_0)(x - x_1) + \cdots + a_n(x - x_0) \cdots (x - x_{n-1})

    Therefore the constants :math:`a_0, a_1, \cdots, a_n` must be found to construct the polynomial. To
    find these constants, the divided differences are recursively generated until :math:`n` iterations
    have been completed. We start with the zeroth divided difference of the function :math:`f` with
    respect to :math:`x_i`, which is the value of :math:`f` at that point. Bracket notation is introduced
    to distinguish the divided differences.

    .. math::

        f[x_i] = f(x_i)

    The first divided difference is then the function :math:`f` with respect to the values :math:`x_i`
    and :math:`x_{i+1}`.

    .. math::

        f[x_i, x_{i+1}] = \frac{f[x_{i+1}] - f[x_i]}{x_{i+1 - x_i}}

    The second divided difference follows:

    .. math::

        f[x_i, x_{i+1}, x_{i+2}] = \frac{f[x_{i+1},x_{i+2}] - f[x_i, x_{i+1}]}{x_{i+2} - x_i}

    This iteration continues until the :math:`n`th divided difference:

    .. math::

        f[x_0, x_1, \cdots, x_n] = \frac{f[x_1, x_2, \cdots, x_n] - f[x_0, x_1, \cdots, x_n]}{x_n - x_0}

    Thus the interpolating polynomial resulting from the divided differences method takes the form:

    .. math::

        P_n(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \cdots +
        f[x_0, x_1, x_2, \cdots, x_n](x - x_0)(x - x_1) \cdots (x - x_{n-1})

    Examples
    --------
    >>> x, y = [8.1, 8.3, 8.6, 8.7], [16.9446, 17.56492, 18.50515, 18.82091]
    >>> divided_differences(x, y, 8.4)
    {'Approximated Value of Interpolated Polynomial': 17.8770925200000,
     'Divided Differences Table': array([[  1.69446000e+01,   0.00000000e+00,   0.00000000e+00,
               0.00000000e+00],
            [  1.75649200e+01,   3.10160000e+00,   0.00000000e+00,
               0.00000000e+00],
            [  1.85051500e+01,   3.13410000e+00,   6.50000000e-02,
               0.00000000e+00],
            [  1.88209100e+01,   3.15760000e+00,   5.87500000e-02,
              -1.04166667e-02]]),
     'Interpolated Function': '16.9446 + 3.1016*(x - 8.1) + 0.065*(x - 8.1)*(x - 8.3) + -0.01042*(x - 8.1)*(x - 8.3)*(x - 8.6)'}

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    """
    x, y = _create_array(x)[0], _create_array(y)[0]

    if len(x) != len(y):
        raise ValueError('x and y must be the same length to evaluate polynomial')

    n = len(x)

    q = np.zeros((n, n))
    q[:, 0] = y

    f = str(np.round(q[0, 0], 5))
    fi = ''

    for i in np.arange(1, n):
        for j in np.arange(i, n):
            q[j, i] = (q[j, i-1] - q[j-1, i-1]) / (x[j] - x[j-i])

        fi = fi + '*(x - ' + str(x[i-1]) + ')'
        f = f + ' + ' + str(np.round(q[i,i], 5)) + fi

    x = Symbol('x')
    if x0 is None:
        raise ValueError('x0 must be provided to approximate polynomial')
    else:
        approx = parse_expr(f).evalf(subs={x: x0})

    res = {'Approximated Value of Interpolated Polynomial': approx,
           'Interpolated Function': f,
           'Divided Differences Table': q}

    return res


# def taylorseries(f, x0):
#     r"""
#
#     Parameters
#     ----------
#     f
#     x0
#
#     Returns
#     -------
#
#     Examples
#     --------
#     >>> def f(x): return 3 * x ** 5 - 2 * x ** 4 + 15 * x ** 3 + 13 * x ** 2 - 12 * x - 5
#
#     """
#     x = Symbol('x')
#     a = f(x)
#
#     deg = degree(a)
#     coefs = []
#
#     for i in range(deg + 1):
#         coefs.append(float(a.evalf(subs={x: x0})))
#         a = diff(a)
#
#     taylorf = int(coefs[0])
#     for i in range(1, len(coefs)):
#         taylorf = str(f) + ' + ' + str(int(coefs[i]  / factorial(i))) + '(x - ' + str(2) + ') **m ' + str(i)
#
#     return taylorf
