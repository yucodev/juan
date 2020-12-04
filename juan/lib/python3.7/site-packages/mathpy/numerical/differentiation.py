# encoding=utf8

"""
Module containing functions and methods for approximating the derivative of functions

"""

import numpy as np

from mathpy._lib import _create_array


def forward_difference(x, y):
    r"""
    Approximates the derivative of an unknown function given a set of x
    and y = f(x) data points using the forward-difference approximation method. The
    x-values should be equally-spaced for the central difference method to return
    accurate results. Otherwise, the forward or backward difference methods should
    be employed (or a more accurate method altogether).

    Parameters
    ----------
    x : array-like
        Pandas DataFrame or Series, Numpy array, list or dictionary of x values
    y : array-like
        Pandas DataFrame or Series, Numpy array, list or dictionary of values of the
        function at x.

    Returns
    -------
    dict
        length :math:`n - 1` where :math:`n` is the length of the data vector x of the
        approximated values of the derivative function at the corresponding values of x.

    Notes
    -----
    The derivative of a function :math:`f` at a value :math:`x_0` is defined by:

    .. math::

        f^\prime(x_0) = \underset{h \rightarrow 0}{lim} \frac{x_0 + h) - f(x_0)}{h}

    However, if the function is unknown, the derivative of the function can still be approximated
    at a value of :math:`x_0` given a set of points :math:`(x_1, y_1), (x_2, y_2), \cdots, (x_n, y_n)`.
    The forward difference method is one approach to approximating the derivative. Given a set of data
    points, the forward difference approximation of a derivative can be defined as:

    .. math::

        f^\prime (x_i) = y^\prime_i \approx \frac{y_{i+1} - y_i}{x_{i+1} - x_i}

    Examples
    --------
    >>> x, y = [0.0, 0.2, 0.4], [0.00000, 0.74140, 1.3718]
    >>> forward_difference(x, y)
    {'f(0.0)': 3.7069999999999994,
     'f(0.2)': 3.7069999999999994,
     'f(0.4)': 3.1519999999999997}
    >>> forward_difference([0.5,0.6,0.7], [0.4794,0.5646,0.6442])
    {'f(0.5)': 0.8520000000000002,
     'f(0.6)': 0.8520000000000002,
     'f(0.7)': 0.79600000000000026}

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Finite difference. (2017, June 9). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Finite_difference&oldid=784585490

    """
    x, y = _create_array(x)[0], _create_array(y)[0]

    if len(x) != len(y):
        raise ValueError('x and y must be the same length')

    n = len(x)

    fdx = {}

    fdx['f(' + str(x[0]) + ')'] = (y[1] - y[0]) / (x[1] - x[0])

    for i in np.arange(1, n):
        fdx['f(' + str(x[i]) + ')'] = (y[i - 1] - y[i]) / (x[i - 1] - x[i])

    return fdx


def backward_difference(x, y):
    r"""
    Approximates the derivative of an unknown function given a set of x
    and y = f(x) data points using the backward-difference approximation method.

    Parameters
    ----------
    x : array-like
        Pandas DataFrame or Series, Numpy array, list or dictionary of x values
    y : array-like
        Pandas DataFrame or Series, Numpy array, list or dictionary of values of the
        function at x.

    Returns
    -------
    dict
        length :math:`n - 1` where :math:`n` is the length of the data vector x of the
        approximated values of the derivative function at the corresponding values of x.

    Notes
    -----
    The derivative of a function :math:`f` at a value :math:`x_0` is defined by:

    .. math::

        f^\prime(x_0) = \underset{h \rightarrow 0}{lim} \frac{x_0 + h) - f(x_0)}{h}

    The backward difference method is one approach to approximating the derivative of a function,
    whether known or unknown. Given a set of data points, the backward difference approximation
    of a derivative can be defined as:

    .. math::

        f^\prime (x_i) = y^\prime_i \approx \frac{y_i - y_{i-1}}{x_i - x_{i-1}}

    Examples
    --------
    >>> x, y = [0.0, 0.2, 0.4], [0.00000, 0.74140, 1.3718]
    >>> backward_difference(x, y)
    {'f(0.0)': 3.7069999999999994,
     'f(0.2)': 3.1519999999999997,
     'f(0.4)': 3.1519999999999997}
    >>> backward_difference([0.5,0.6,0.7], [0.4794,0.5646,0.6442])
    {'f(0.5)': 0.8520000000000002,
     'f(0.6)': 0.79600000000000026,
     'f(0.7)': 0.79600000000000026}

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Finite difference. (2017, June 9). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Finite_difference&oldid=784585490

    """
    x, y = _create_array(x)[0], _create_array(y)[0]

    if len(x) != len(y):
        raise ValueError('x and y must be the same length')

    n = len(x)

    fdx = {}

    for i in np.arange(1, n):
        fdx['f(' + str(x[i - 1]) + ')'] = (y[i] - y[i - 1]) / (x[i] - x[i - 1])

    fdx['f(' + str(x[n - 1]) + ')'] = fdx['f(' + str(x[n - 2]) + ')']

    return fdx


def central_difference(x, y):
    r"""
    Approximates the derivative of an unknown function given a set of x
    and y = f(x) data points using the central-difference approximation method.

    Parameters
    ----------
    x : array-like
        Pandas DataFrame or Series, Numpy array, list or dictionary of x values
    y : array-like
        Pandas DataFrame or Series, Numpy array, list or dictionary of values of the
        function at x.

    Returns
    -------
    dict
        length :math:`n - 1` where :math:`n` is the length of the data vector x of the
        approximated values of the derivative function at the corresponding values of x.

    Notes
    -----
    The derivative of a function :math:`f` at a value :math:`x_0` is defined by:

    .. math::

        f^\prime(x_0) = \underset{h \rightarrow 0}{lim} \frac{x_0 + h) - f(x_0)}{h}

    The central-difference method is another approach to approximating the derivative of a function,
    whether it be a known function or a set of points and the function evaluated at those points. The
    central-difference formula is defined as:

    .. math::

        f^\prime (x_i) = \frac{f(x + h) - f(x - h)}{2h}

    The central-difference method is often more accurate than the backward or forward methods as it is
    essentially an average of the latter two approaches.

    Examples
    --------
    >>> x, y = [0.0, 0.2, 0.4], [0.00000, 0.74140, 1.3718]
    >>> central_difference(x, y)
    {'f(0.0)': 3.7069999999999994,
     'f(0.2)': 3.7069999999999994,
     'f(0.4)': 3.1519999999999997}
    >>> central_difference([0.5,0.6,0.7], [0.4794,0.5646,0.6442])
    {'f(0.5)': 0.8520000000000002,
     'f(0.6)': 0.8520000000000002,
     'f(0.7)': 0.79600000000000026}

    References
    ----------
    Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Finite difference. (2017, June 9). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Finite_difference&oldid=784585490

    """
    x, y = _create_array(x)[0], _create_array(y)[0]

    if len(x) != len(y):
        raise ValueError('x and y must be the same length')

    n = len(x)

    fdx = {}

    fdx['f(' + str(x[0]) + ')'] = ((y[1] - y[0]) - (y[0] - y[1])) / (2 * (x[1] - x[0]))

    for i in np.arange(1, n):
        fdx['f(' + str(x[i]) + ')'] = ((y[i] - y[i - 1]) - (y[i - 1] - y[i])) / (2 * (x[i] - x[i - 1]))

    return fdx


def approximate_derivative_finite(f, x, method='central'):
    r"""
    Approximates the derivative of a given function at a value of x using either the
    central (default), forward or backward forms of the finite differences method.

    Parameters
    ----------
    f : function
        Given function to approximate derivative at supplied value of :math:`x`. Must be
        a callable function with one parameter representing a single variable function.
    x : float, int
        Value at which to approximate the derivative of the given function
    method : {'central', 'forward', 'backward'}
        Method to use to approximate the derivative. The default is the central method which
        generally reports a smaller error compared to the forward and backward methods.

    Returns
    -------
    tuple
        First element is the approximated value of the derivative of the function at the given
        value of :math:`x` and the error bound.

    Notes
    -----
    The derivative of a function :math:`f` at a value :math:`x_0` is defined by:

    .. math::

        f^\prime(x_0) = \underset{h \rightarrow 0}{lim} \frac{x_0 + h) - f(x_0)}{h}

    This allows the approximation of :math:`f^\prime (x_0) for small values of :math:`h`. This
    approximation can be faulty due to round-off error and is therefore not a good method to use
    in practicality; however, it suffices for a quick and comparatively easy approximation. There
    are three primary forms of finite differences; central, forward, and backward.

    The forward difference can be expressed as:

    .. math::

        f^\prime (x) = \frac{f(x + h) - f(x)}{h}

    The backward difference is expressed slightly different than the forward method:

    .. math::

        f*\prime (x) = \frac{f(x) - f(x - h)}{h}

    The central difference is essentially an average of the backward and forward method and
    can bee expressed as:

    .. math::

        f*\prime (x) = \frac{f(x + \frac{1}{2}h) - f(x - \frac{1}{2}h)}{h}

    Examples
    --------
    >>> def f(x): return np.exp(x) - 2 * x ** 2 + 3 * x - 1
    >>> approximate_derivative_finite(f, 0.2)
    3.4214025940746069
    >>> approximate_derivative_finite(f, 0.2, 'backward')
    3.4214029237627983

    References
    ----------
     Burden, R. L., & Faires, J. D. (2011). Numerical analysis (9th ed.).
        Boston, MA: Brooks/Cole, Cengage Learning.

    Finite difference. (2017, June 9). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Finite_difference&oldid=784585490

    """
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')

    h = np.finfo(np.float32).eps

    if method is None or method == 'central':
        fdx =(f(x + 0.5 * h) - f(x - 0.5 * h)) / h

    elif method == 'forward':
        fdx = (f(x + h) - f(x)) / h

    elif method == 'backward':
        fdx = (f(x) - f(x - h)) / h

    else:
        raise ValueError('method must be None or one of {"central", "forward", "backward"}')

    return fdx
