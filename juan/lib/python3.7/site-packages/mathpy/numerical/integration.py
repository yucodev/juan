# encoding=utf8

"""
Module containing functions and methods for approximating the integral of functions

"""

import numpy as np


def trapezoidal_rule(f, a, b):
    r"""
    Approximates the integral of a function over the interval :math:`[a, b]` using the
    Trapezoidal Rule.

    Parameters
    ----------
    f : function
        Given function to approximate derivative at supplied value of :math:`x`. Must be
        a callable function with one parameter representing a single variable function.
    a : int or float
        The lower value of the integral to approximate
    b : int or float
        The upper lower of the integral to approximate

    Returns
    -------
    float
        The approximated value of the function integrated over the interval :math:`[a, b]`.

    Notes
    -----
    The Trapezoidal Rule gives an approximation of the integral of a function over the interval
    :math:`[a, b]`. The Trapezoidal Rule is defined as:

    .. math::

        \int^a_b f(x) dx = \frac{h}{2}[f(x_0) + f(x_1)] - \frac{h^3}{12} f^{\prime \prime} (\epsilon)

    Where :math:`- \frac{h^3}{12} f^{\prime \prime} (\epsilon)` is the error term. The Trapezoidal Rule
    approximates the integral :math:`\int^a_b f(x) dx` by using the area of a trapezoid, hence its name.

    Examples
    --------
    >>> def f(x): return x ** 4
    >>> trapezoidal_rule(f, 0.5, 1)
    .265625
    >>> def f2(x): return 2 / (x - 4)
    >>> trapezoidal_rule(f2, 0, 0.5)
    -.2678571

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    """
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')
    if isinstance(a, float) is False:
        a = float(a)
    if isinstance(b, float) is False:
        b = float(b)

    h = b - a

    approx = (h / 2.) * (f(a) + f(b))

    return approx


def composite_trapezoidal(f, a, b, n=6):
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')

    h = (b - a) / n

    xj = np.linspace(a, b, n + 1)

    return (h / 2) * (f(a) + 2 * np.sum(f(xj[1:-1])) + f(b))

def simpsons_rule(f, a, b):
    r"""
    Approximates the integral of a function over the interval :math:`[a, b]` using Simpson's
    Rule.

    Parameters
    ----------
    f : function
        Given function to approximate derivative at supplied value of :math:`x`. Must be
        a callable function with one parameter representing a single variable function.
    a : int or float
        The lower value of the integral to approximate
    b : int or float
        The upper lower of the integral to approximate

    Returns
    -------
    float
        The approximated value of the function integrated over the interval :math:`[a, b]`.

    Notes
    -----
    Simpson's rule is another method in numerical analysis for approximating the definite
    integral of a function. The rule is defined as:

    .. math::

        \int_{x_0}^{x_2} f(x) dx = \frac{h}{3}[f(x_0) + 4f(x_1) + f(x_2)] - \frac{h^5}{90}f^{(4)} (\epsilon)

    Where :math:`\frac{h^5}{90}f^{(4)} (\epsilon)` is the error term.

    Examples
    --------
    >>> def f(x): return x ** 4
    >>> simpsons_rule(f, 0.5, 1)
    .1940104
    >>> def f2(x): return 2 / (x - 4)
    >>> simpsons_rule(f2, 0, 0.5)
    -.2670635

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    """
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')

    if isinstance(a, float) is False:
        a = float(a)
    if isinstance(b, float) is False:
        b = float(b)

    h = (b - a) / 2.
    x0, x1, x2 = a, a + h, b

    approx = (h / 3.) * (f(x0) + 4. * f(x1) + f(x2))

    return approx

def composite_simpsons_rule(f, a, b, n=6):
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')

    h = (b - a) / n

    xj = np.linspace(a, b, n + 1)[1:-1]

    return (h / 3) * (f(a) + 2 * np.sum(f(xj[1::2])) + 4 * np.sum(f(xj[0::2])) + f(b))
