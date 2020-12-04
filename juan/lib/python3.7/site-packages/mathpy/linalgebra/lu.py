# encoding=utf8


"""
Module containing implementations of Cholesky decomposition for symmetric,
positive-definite matrices.

"""

import numpy as np
import pandas as pd
from mathpy._lib import _create_array
from mathpy.linalgebra.matrix import ispositivedefinite


def cholesky(a):
    r"""
    Function for computing the Cholesky decomposition of a symmetric, positive definite matrix.

    Parameters
    ----------
    a : array_like
        Accepts a list, nested list, dictionary, pandas DataFrame or
        pandas Series. The private function _create_array is called
        to create a copy of x as a numpy array.

    Returns
    -------
    llt : tuple
        The cholesky function returns the lower-triangular matrix L and its transpose,
        the upper-triangular matrix L^T.

    Notes
    -----
    Cholesky decomposition is a special case of :math:`LU` decomposition for symmetric,
    positive definite matrices (Hermitian in the complex case). Cholesky decomposition is
    preferred when applicable as it is more efficient than LU decomposition. The Cholesky
    decomposition factors a matrix :math:`A` into the product of a lower triangular matrix
    :math:`L` and its transpose :math:`L^T` (or :math:`L^*` which denotes the conjugate
    transpose in the Hermitian case). More formally, for a symmetric, positive definite
    matrix :math:`A`, the Cholesky decomposition is defined as:

    .. math::

        A = LL^T

    In component notation:

    .. math::

        L_{ii} = \sqrt{a_{ii} - \sum^{i-1}_{k=0} L^2_{ik}}

    .. math::

        L_{ji} = \frac{1}{L_{ii}} (a_{ij} - \sum^{i-1}_{k=0} L_{ik} L_{jk}) \qquad j = i + 1, i + 2, \cdots, N - 1

    Examples
    --------
    >>> h = pd.DataFrame({0: [16, 4, 8, 4], 2: [4, 10, 8, 4], 3: [8, 8, 12, 10], 4: [4, 4, 10, 12]})
    >>> l, lt = cholesky(h)
    >>> l
    array([[4, 0, 0, 0],
       [1, 3, 0, 0],
       [2, 2, 2, 0],
       [1, 1, 3, 1]], dtype=int64)
    >>> lt
    array([[4, 1, 2, 1],
       [0, 3, 2, 1],
       [0, 0, 2, 3],
       [0, 0, 0, 1]], dtype=int64)

    References
    ----------
    Press, W. (2007). Numerical Recipes 3rd Edition: The Art of Scientific Computing (3rd ed.).
        New York: Cambridge University Press.

    Watkins, D. (2010). Fundamentals of Matrix Computations, 3rd Edition. John Wiley & Sons.

    """
    x = _create_array(a)[0].copy()
    n, m = x.shape

    if ispositivedefinite(x) is False:
        raise ValueError('Matrix is not positive definite')

    for j in np.arange(n):

        x[j, j] = np.sqrt(x[j, j] - np.dot(x[j, 0: j], x[j, 0: j]))
        for i in np.arange(j + 1, n):
            x[i, j] = (x[i, j] - np.dot(x[i, 0:j], x[j, 0: j])) / x[j, j]

    for j in np.arange(1, n):
        x[0: j, j] = 0.0

    llt = (x, x.T)

    return llt


def lu(a):
    r"""
    Computes the LU decomposition of a square matrix :math:`A`.

    Parameters
    ----------
    a : array_like
        Accepts a list, nested list, dictionary, pandas DataFrame or
        pandas Series. The private function _create_array is called
        to create a copy of x as a numpy array.

    Returns
    -------
    l_u : tuple
        Returns a tuple containing the lower triangular matrix
        :math:`L` and the upper triangular matrix  :math:`U`.

    Notes
    -----
    LU Decomposition factors a square matrix (:math:`n \times n`) into the product of a
    'lower' and 'upper' triangular matrix (hence the name 'LU'). More formally:

    .. math::

        A = LU

    The :math:`L` and :math:`U` matrices are lower and upper triangular, respectively.
    For example, the LU decomposition of a :math:`3 \times 3` matrix would be similar to:

    .. math::

        \begin{bmatrix}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23} \\
            a_{31} & a_{32} & a_{33}
        \end{bmatrix} =
        \begin{bmatrix}
            l_{11} & 0 & 0 \\
            l_{21} & l_{22} & 0 \\
            l_{31} & l_{32} & l_{33}
        \end{bmatrix}
        \begin{bmatrix}
            u_{11} & u_{12} & u_{13} \\
            0 & u_{22} & u_{23} \\
            0 & 0 & u_{33}
        \end{bmatrix}

    Examples
    --------
    >>> a = pd.DataFrame({0: [16, 4, 8, 4], 2: [4, 10, 8, 4], 3: [8, 8, 12, 10], 4: [4, 4, 10, 12]})
    >>> l, u = lu(a)
    >>> print(l, u)
    [[ 1.          0.          0.          0.        ]
     [ 0.25        1.          0.          0.        ]
     [ 0.5         0.66666667  1.          0.        ]
     [ 0.25        0.33333333  1.5         1.        ]] [[ 16.   4.   8.   4.]
     [  0.   9.   6.   3.]
     [  0.   0.   4.   6.]
     [  0.   0.   0.   1.]]
    >>> np.dot(l, u)
    array([[ 16.,   4.,   8.,   4.],
       [  4.,  10.,   8.,   4.],
       [  8.,   8.,  12.,  10.],
       [  4.,   4.,  10.,  12.]])

    References
    ----------
    Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). Introduction to algorithms (3rd ed., pp. 819-822).
        Cambridge (Inglaterra): Mit Press.

    """
    x = _create_array(a)[0].copy()
    n, m = x.shape

    if n != m:
        raise ValueError('Matrix must be square to perform LU decomposition')

    l, u = np.eye(n), np.zeros((n, n))

    for k in np.arange(n):
        u[k,k] = x[k,k]
        for i in np.arange(k+1, n):
            l[i,k] = x[i,k] / u[k,k]
            u[k,i] = x[k,i]
        for i in np.arange(k+1, n):
            for j in np.arange(k+1, n):
                x[i,j] = x[i,j] - l[i,k] * u[k,j]

    l_u = (l, u)

    return l_u
