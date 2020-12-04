# encoding=utf8


"""
Module containing several functions for testing if a matrix is symmetric, positive definite, orthogonal, etc.

"""

import numpy as np
import pandas as pd
from mathpy._lib import _create_array


def issymmetric(x):
    r"""
    Tests if a matrix is symmetric.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is symmetric

    Notes
    -----
    A symmetric matrix is defined as a square matrix that is equal to its transpose.

    .. math::

        A \in \mathbb{R}^{n \times n} \qquad A^T = A

    A symmetric matrix has the following form:

    .. math::

        \begin{bmatrix}
            a_{11} & a_{12} & \cdots & a_{1n} \\
            a_{12} & a_{22} & \cdots & a_{2n} \\
            \vdots & \vdots & \ddots & \vdots \\
            a_{1n} & a_{2n} & \cdots & a_{nn}
        \end{bmatrix}

    Examples
    --------
    >>> m = pd.DataFrame({0: [2,-1,0], 1: [-1,2,-1], 2: [0,-1,2]})
    >>> issymmetric(m)
    True

    References
    ----------
    Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

    Weisstein, Eric W. "Symmetric Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/SymmetricMatrix.html

    """
    x = _create_array(x)[0]

    if x.shape[0] != x.shape[1]:
        return False

    if np.allclose(np.transpose(x), x) is False:
        return False

    return True


def isskewsymmetric(x):
    r"""
    Tests if a matrix is skew symmetric.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is antisymmetric

    Notes
    -----
    Skew symmetric matrices are also known as antisymmetric. A skew symmetric matrix is equal to its
    negative transpose.

    .. math::

        A = -A^T

    :math:`a_{ij}` must equal :math:`-a_{ji}`, thus the diagonal of a skew symmetric matrix must be 0,
    as :math:`a_{jj}` = :math:`-a_{jj}`.

    .. math::

        \begin{bmatrix}
            0 & a_{12} & a_{13} \\
            -a_{12} & 0 & a_{23} \\
            -a_{13} & -a_{23} & 0
        \end{bmatrix}

    Examples
    --------
    >>> m = pd.DataFrame({0: [0,-2,1], 1: [2,0,4], 2: [-1,-4,0]})
    >>> isskewsymmetric(m)
    True
    >>> m2 = pd.DataFrame({0: [2,-1,0], 1: [-1,2,-1], 2: [0,-1,2]})
    >>> isskewsymmetric(m2)
    False

    References
    ----------
    Rowland, Todd and Weisstein, Eric W. "Antisymmetric Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/AntisymmetricMatrix.html

    """
    x = _create_array(x)[0]

    if x.shape[0] != x.shape[1]:
        return False

    if np.allclose(x, -np.transpose(x)) is False:
        return False

    return True


def ispositivedefinite(x):
    r"""
    Tests if a real matrix is positive definite. Complex matrices are currently not supported.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is positive definite

    Notes
    -----
    A real matrix :math:`A` is positive definite if:

    .. math::

        x^T Ax > 0

    where x^T denotes the transpose.

    Examples
    --------
    >>> m = pd.DataFrame({0: [2,-1,0], 1: [-1,2,-1], 2: [0,-1,2]})
    >>> ispositivedefinite(m)
    True

    References
    ----------
    Weisstein, Eric W. "Positive Definite Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/PositiveDefiniteMatrix.html

    """
    if issymmetric(x) is False:
        return False

    e = _sym_eig(x)

    for i in e:
        if i < 0:
            return False

    return True


def ispositivesemidefinite(x):
    r"""
    Tests if a matrix is positive semidefinite. Complex and Hermitian matrices are currently not supported.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is positive semidefinite

    Notes
    -----
    A Hermitian matrix (or symmetric real matrix if there are no complex entries) is defined
    as positive semidefinite if all its eigenvalues are non-negative.

    Examples
    --------
    >>> m = pd.DataFrame({0: [2,-1,0], 1: [-1,2,-1], 2: [0,-1,2]})
    >>> ispositivesemidefinite(m)
    True

    References
    ----------
    Weisstein, Eric W. "Positive Semidefinite Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/PositiveSemidefiniteMatrix.html

    """
    if issymmetric(x) is False:
        return False

    e = _sym_eig(x)

    for i in e:
        if i < 0:
            return False

    return True


def isnegativedefinite(x):
    r"""
    Tests if a matrix is negative definite. Complex matrices are currently not supported.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is negative definite

    Notes
    -----
    A Hermitian matrix (or symmetric real matrix if there are no complex entries) is defined
    as negative definite if all its eigenvalues are negative.

    Examples
    --------
    >>> m = pd.DataFrame({0: [2,-1,0], 1: [-1,2,-1], 2: [0,-1,2]})
    >>> isnegativedefinite(m)
    True
    >>> a = pd.DataFrame({0: [-3,0,0], 1: [0,-2,0], 2: [0,0,-1]})
    >>> isnegativedefinite(a)
    True

    References
    ----------
    Weisstein, Eric W. "Negative Definite Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/NegativeDefiniteMatrix.html

    """
    if issymmetric(x) is False:
        return False

    e = _sym_eig(x)

    for i in e:
        if i >= 0:
            return False

    return True


def isnegativesemidefinite(x):
    r"""
    Tests if a matrix is negative semidefinite. Complex matrices are currently not supported.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is negative semidefinite

    Notes
    -----
    A Hermitian matrix (or symmetric real matrix if there are no complex entries) is defined
    as negative semidefinite if all its eigenvalues are nonpositive.

    Examples
    --------
    >>> b = list([0,0], [0,-1])
    >>> isnegativesemidefinite(b)
    True

    References
    ----------
    Weisstein, Eric W. "Negative Semidefinite Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/NegativeSemidefiniteMatrix.html

    """
    if issymmetric(x) is False:
        return False

    e = _sym_eig(x)

    for i in e:
        if i >= 0:
            return False

        return True


def isindefinite(x):
    r"""
    Tests if a matrix is indefinite.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is indefinite

    Notes
    -----
    An indefinite matrix is defined as a square matrix with real or complex entries with a non-zero
    determinant that is neither positive definite or negative definite.

    References
    ----------
    Weisstein, Eric W. "Indefinite Matrix." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/IndefiniteMatrix.html

    """
    if ispositivedefinite(x) is not True and ispositivesemidefinite(x) is not True and \
            isnegativedefinite(x) is not True and isnegativesemidefinite(x) is not True:
        return True
    else:
        return False


def isorthogonal(x):
    r"""
    Tests if a matrix is orthogonal.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    Boolean
        Returns True if matrix is orthogonal

    Notes
    -----
    A square matrix :math:`A` is said to be orthogonal if:

    .. math::

        AA^T = I

    Where :math:`A^T` is the transpose of :math:`A` and :math:`I` is the identity matrix.

    The following matrix is orthogonal:

    .. math::

        A = \begin{bmatrix}\frac{1}{3} & -\frac{2}{3} & \frac{2}{3} \\
        \frac{2}{3} & -\frac{1}{3} & -\frac{2}{3} \\
        \frac{2}{3} & \frac{2}{3} & \frac{1}{3} \end{bmatrix}

    Examples
    --------
    >>> a = pd.DataFrame({0: [1/3, 2/3, 2/3], 1: [-2/3, -1/3, 2/3], 2: [2/3,-2/3,1/3]})
    >>> isorthogonal(a)
    True

    References
    ----------
    Rowland, Todd. "Orthogonal Matrix." From MathWorld--A Wolfram Web Resource, created by Eric W. Weisstein.
        http://mathworld.wolfram.com/OrthogonalMatrix.html

    """
    x = _create_array(x)[0]

    if x.shape[0] != x.shape[1]:
        return 'Matrix is not orthogonal'

    if np.allclose(np.dot(x, x.T), np.eye(x.shape[0])):
        return True

    return False


def _sym_eig(x):
    x = _create_array(x)[0]
    eigs = np.linalg.eigvals(x)

    return eigs
