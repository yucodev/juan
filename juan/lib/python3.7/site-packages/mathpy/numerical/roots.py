# encoding=utf8


"""
Module containing functions for approximating the roots of functions.

"""

from sympy import diff, var, symbols
import numpy as np
from collections import namedtuple


def newtonraph(f, x0, tol=1.0e-9, n=1000):
    r"""
    Implementaion of the Newton-Raphson method for approximating a root with
    an initial guess x0.

    Parameters
    ----------
    f : function
        The polynomial function to be evaluated. For example, to evaluate the
        polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, f should be similar to:

        .. code-block:: python

            def f(x):
                # The variable in function f must be set as x.
                return 3 * x ** 3 - 5 * x ** 2 + 2 * x - 1

    x0 : int or float
        The initial guess of the function's root.
    tol : float default 1.0e-9
        The level of error tolerance between the approximated root and the
        actual root.
    n : int default 1000
        Number of iterations.

    Returns
    -------
    x0 : int or float
        If the function evaluated at x0 is 0, the root is located at x0 and is
        returned by the function.
    root : namedtuple
        approx is the approximate root of the function in the interval between
        a and b, iter is a list of the previous iterations, and count is the
        number of iterations before reaching the root approximation.

    Notes
    -----
    The Newton-Raphson is a root-finding method that is generally fast in
    convergence given the initial guess to the root is well chosen. Thus,
    plotting the function before utilizing the Newton-Raphson method is
    often recommended to get a good initial guess by observation.

    The Newton-Raphson method starts with an initial guess (hopefully close
    to the true root), the function f is then approximated by its tangent line.
    The tangent line to the curve :math:`y=f(x)` at the point :math:`x = x_n` is
    defined as:

    .. math::

        y = f'(x_n)(x - x_n) + f(x_n)

    The x-intercept of the tangent line is then set as the next approximation to
    the true root of the function. This leads to the Newton-Raphson iteration,
    defined as:

    .. math::

        x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}

    Examples
    --------
    >>> def f(x): return x ** 3 - 2 * x - 5
    >>> root, iters, niter = newtonraph(f, 2)
    >>> root
    2.09455148154233
    >>> iters
    [2.10000000000000, 2.09456812110419, 2.09455148169820, 2.09455148154233]
    >>> niter
    4

    >>> def f2(x): return x ** 2 - 10
    >>> root2, iters2, niter2 = newtonraph(f2, 3)
    >>> root2
    3.16227766016838
    >>> iters2
    [3.16666666666667, 3.16228070175439, 3.16227766016984, 3.16227766016838]
    >>> niter2
    4

    References
    ----------
    Newton's method. (2017, April 23). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Newton%27s_method&oldid=776802339

    Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
        Cambridge: Cambridge University Press.

    Weisstein, Eric W. "Newton's Method." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/NewtonsMethod.html

    """
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')

    x = var('x')

    root = namedtuple('root', 'approx iter count')
    k = []

    fx0 = f(x0)
    if fx0 == 0.0:
        return fx0

    for i in np.arange(n):
        dfx = diff(f(x))
        dx = dfx.evalf(subs={x: x0})
        x1 = x0 - (f(x0) / dx)
        k.append(x1)

        if abs(x1 - x0) < tol:
            return root(approx=k[i], iter=k, count=len(k))
        x0 = x1

    raise ValueError('Iteration limit exceeded')


def bisection(f, a, b, tol=1.0e-9, n=1000):
    r"""
    Implements the bisection method of approximating a root within a given
    interval :math:`[a, b]`.

    Parameters
    ----------
    f : function
        The polynomial function to be evaluated. For example, to evaluate the
        polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, f should be similar to:

        .. code-block:: python

            def f(x):
                # The variable in function f must be set as x.
                return 3 * x^3 - 5 * x^2 + 2 * x - 1

    a : int or float
        The lower bound of the interval in which to search for the root.
    b: int or float
        The upper bound of the interval in which to search for the root.
    tol : float default 1.0e-9
        The level of error tolerance between the approximated root and the
        actual root.
    n : int default 1000
        Number of iterations.

    Returns
    -------
    root : namedtuple
        approx is the approximate root of the function in the interval between
        a and b, iter is a list of the previous iterations, and count is the
        number of iterations before reaching the root approximation.

    Notes
    -----
    The bisection method is another approach to finding the root of a continuous
    function :math:`f(x)` on an interval :math:`[a, b]`. The method takes advantage of a
    corollary of the intermediate value theorem called Bolzano's theorem which
    states that if the values of :math:`f(a)` and :math:`f(b)` have opposite signs, the
    interval must contain at least one root. The iteration steps of the bisection
    method are relatively straightforward, however; convergence towards a solution
    is slow compared to other root-finding methods.

    Examples
    --------
    >>> def f(x): return x ** 3 - 2 * x - 5
    >>> root, iters, niter = bisection(f, 2, 2.2)
    >>> root
    2.094551482051611
    >>> iters
    [2.1,
     2.05,
     2.075,
     2.0875000000000004,
     2.09375,
     2.096875,
     2.0953125,
     2.09453125,
     2.094921875,
     2.0947265625,
     2.09462890625,
     2.0945800781250004,
     2.0945556640625003,
     2.09454345703125,
     2.0945495605468754,
     2.094552612304688,
     2.0945510864257817,
     2.094551849365235,
     2.094551467895508,
     2.0945516586303716,
     2.09455156326294,
     2.094551515579224,
     2.094551491737366,
     2.0945514798164373,
     2.0945514857769014,
     2.0945514827966694,
     2.0945514813065533,
     2.094551482051611]
     >>> niter
     28

    References
    ----------
    Bisection method. (2017, April 21). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Bisection_method&oldid=776568784

    Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
        Cambridge: Cambridge University Press.

    Weisstein, Eric W. "Bisection." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/Bisection.html

    """
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')
    if (f(a) < 0 and f(b) < 0) or (f(a) > 0 and f(b) > 0):
        raise ValueError('signs of function evaluated at points a and b must differ')

    root = namedtuple('root', 'approx iter count')
    k = []

    for _ in np.arange(n):
        c = float(a + b) / 2.0
        k.append(c)
        if f(c) == 0 or float(b - a) / 2.0 < tol:
            return root(approx=c, iter=k, count=len(k))

        if np.sign(f(c)) == np.sign(f(a)):
            a = c
        else:
            b = c

    raise ValueError('Iteration limit exceeded without convergence')


def secant(f, x0, x1, tol=1.0e-9, n=1000):
    r"""
    Approximates a root of a function using the secant method given two
    initial guesses ideally located near the true root.

    Parameters
    ----------
    f : function
        The polynomial function to be evaluated. For example, to evaluate the
        polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, f should be similar to:

        .. code-block:: python

            def f(x):
                # The variable in function f must be set as x.
                return 3 * x^3 - 5 * x^2 + 2 * x - 1

    x0 : int or float
        Lower bound of the interval in which to search for a root of the function.
        The lower bound should ideally be located close to the true root.
    x1 : int or float
        Upper bound of the interval. The upper bound should ideally be located close
        to the true root.

    Returns
    -------
    root : namedtuple
        approx is the approximate root of the function in the interval between
        a and b, iter is a list of the previous iterations, and count is the
        number of iterations before reaching the root approximation.

    Notes
    -----
    The secant method for finding roots of nonlinear equations is a variation
    of the Newton-Raphson method that takes two initial guesses of the root,
    compared to just one guess required for Newton-Raphson. Due to the extra
    computations as a result of requiring two approximations, the secant method
    often converges more slowly compared to Newton-Raphson; however, it is usually
    more stable. The secant method has another advantage over NR as it does not need
    the derivative of the function in question to be known or assumed to be easily
    calculated. The secant method uses secant lines (hence the need for two initial
    starting values) to find the root of a function while the Newton-Raphson method
    approximates the root with a tangent line.

    The general iteration equation of the secant method given two initial guesses
    :math:`x_0` and :math:`x_1` is defined as:

    .. math::

        x_{n+1} = x_n - f(x_n) \bigg/ \frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}

    Examples
    --------
    >>> def f(x): return x^3 - 2* x - 5
    >>> root, iters, niter = secant(f, 1, 3)
    >>> root
    2.0945514815423265
    >>> iters
    [1.5454545454545454,
     1.8591632292280496,
     2.2003500781687437,
     2.0797991804599714,
     2.09370424253899,
     2.094558562633902,
     2.094551478163657,
     2.094551481542313,
     2.0945514815423265]
    >>> niter
    9
    >>> def f2(x): return x ** 2 - 10
    >>> root2, iters2, niter2 = secant(f2, 3, 4)
    >>> root2
    3.162277660168379
    >>> iters
    [3.142857142857143,
     3.16,
     3.1622846781504985,
     3.1622776576400877,
     3.1622776601683764,
     3.162277660168379]
    >>> niter
    6

    References
    ----------
    Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
        Cambridge: Cambridge University Press.

    Weisstein, Eric W. "Secant Method." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/SecantMethod.html

    """
    if callable(f) is False:
        raise TypeError('f must be a function with one parameter (variable)')

    root = namedtuple('root', 'approx iter count')
    k = []

    for _ in np.arange(n):
        x2 = x1 - f(x1) / (float(f(x1) - f(x0)) / float(x1 - x0))
        k.append(x2)
        if abs(x2 - x1) < tol:
            return root(approx=x2, iter=k, count=len(k))

        x0 = x1
        x1 = x2

    raise ValueError('Iteration limit exceeded without convergence')


#def horner(f, x0, tol=1.0e-9, n=1000):
#     if callable(f) is False:
#         return 'f must be a function'
#
#     x = symbols('x')
