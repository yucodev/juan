# encoding=utf8


"""
Module for computing various vector and matrix norms. Vector norms define a measure
of distance for vectors. Matrix norms are measures of distance in the space of the
matrix. The most common vector norm is the 2-norm, the equivalent matrix norm
is the Frobenius norm.

"""

import numpy as np
from mathpy._lib import _create_array


def norm(x, order=None):
    r"""
    Interface function for computing vector and matrix norms. The default method is
    the 2-norm for vectors and the Frobenius norm for vectors.

    The following vector norm calculations can be performed with the corresponding
    argument to the order parameter.

    ================= ===========
    order             vector norm
    ================= ===========
    None              2-norm
    2 or '2'          2-norm
    1 or '1'          1-norm
    np.inf or 'inf'   inf-norm
    -np.inf or '-inf' -inf-norm
    other             p-norm
    ================= ===========

    The following matrix norm calculations are also available.

    =============== ==============
    order           matrix norm
    =============== ==============
    None            Frobenius norm
    'fro'           Frobenius norm
    'frobenius'     Frobenius norm
    '1' or 1        1-norm
    np.inf or 'inf' inf-norm
    =============== ==============

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.
    order : int or str, optional
        Defaults to the 2-norm computation for vectors and the
        Frobenius norm for matrices. Please refer to the above
        tables for the available norm calculations.

    Returns
    -------
    v : float
        vector or matrix norm of the input

    Notes
    -----
    Please see the respective implementations of the vector and matrix norms
    in the _VectorNorm class.

    Examples
    --------
    >>> v = np.array([5, 2, 1])
    >>> norm(v)
    5.477225575051661
    >>> norm(v, 2)
    5.477225575051661
    >>> norm([5, 2, 1], 'inf')
    5.0
    >>> m = np.array([[2, 1], [1, 2]])
    >>> norm(m)
    3.1622776601683795
    >>> b = np.array([[5, -4, 2], [-1, 2, 3], [-2, 1, 0]])
    >>> norm(b, '1')
    8

    References
    ----------
    Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

    """
    vec_norm = {
        None: 'norm2',
        2: 'norm2',
        '2': 'norm2',
        '1': 'norm1',
        1: 'norm1',
        'inf': 'norminf',
        np.inf: 'norminf',
        '-inf': 'norm_neg_inf',
        -np.inf: 'norm_neg_inf'
    }

    matrix_norm = {
        None: 'frobenius',
        'fro': 'frobenius',
        'frobenius': 'frobenius',
        1: 'norm1',
        '1': 'norm1',
        np.inf: 'norminf',
        'inf': 'norminf'
    }

    x = np.array(x)

    if x.ndim == 1:
        x = _VectorNorm(x)

        try:
            v = getattr(x, vec_norm[order])

        except KeyError:
            if isinstance(order, str):
                try:
                    order = int(order)
                except ValueError:
                    print('unknown norm, ' + str(order) + ' given.')
                    raise

            return x.pnorm(order)

    else:
        x = _MatrixNorm(x)

        try:
            if hasattr(x, matrix_norm[order]):
                v = getattr(x, matrix_norm[order])

        except ValueError:
            print('unknown norm, ' + str(order) + ' given.')
            raise

    return float(v())


class _VectorNorm(object):
    r"""
    Class containing implementations of vector norms used in the
    front-end interface function 'norm'.

    Parameters
    ----------
    x : array_like
        Accepts a list, nested list, dictionary, pandas DataFrame or
        pandas Series. The private function _create_array is called
        to create a copy of x as a numpy array.

    Methods
    -------
    pnorm()
        Calculates the p-norm of a vector.
    norm1()
        Computes the 1-norm of a vector.
    norminf()
        Implements the inf-norm computation of a vector.
    norm2()
        Implements the 2-norm computation.

    Notes
    -----
    Given a vector space :math:`\mathbb{R}^n`, a vector norm is defined as a function :math:`f: \mathbb{R}^n
    \rightarrow \mathbb{R}`. Norms are represented by double-bar notation, for example, a norm :math:`x` would be
    denoted :math:`||x||`. Vector norms have the following properties:

    - :math:`||x|| > 0` for a vector :mat:h`x \in \mathbb{R}^n`
        + :math:`||x|| = 0` if the vector :math:`x = 0`
    - :math:`||\alpha x|| = |\alpha| ||x||` for a vector :math:`x \in \mathbb{R}^n` and a scalar
        :math:`\alpha \in \mathbb{R}`
    - :math:`||x + y|| \leq ||x|| + ||y||` for vectors :math:`x,y \in \mathbb{R}^n`

    References
    ----------
    Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

    """

    def __init__(self, x):
        self.x = _create_array(x)[0]
        self.order = 'norm2'

    def norm2(self):
        r"""
        Computes the 2-norm of a vector.

        Returns
        -------
        l2 : float
            The 2-norm of the vector

        Notes
        -----
        The 2-norm of a vector :math:`x` is defined as:

        .. math::

            ||x||_2 = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2} = \sqrt{x^T x}

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        l2 = np.sqrt(np.sum(np.power(self.x, 2)))

        return l2

    def pnorm(self, p):
        r"""
        Calculates the p-norm of a vector.

        Parameters
        ----------
        p : int
            Used in computing the p-norm. This should only be set
            when calculating the pnorm of a vector is desired.

        Returns
        -------
        pn : float
            The p-norm of the vector.

        Notes
        -----
        The p-norm, which is considered a class of vector norms is defined as:

        .. math::

            ||x||_p = \sqrt[p]{|x_1|^p + |x_2|^p + \cdots + |x_n|^p} \qquad p \geq 1

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        if p != np.floor(p):
            p = np.floor(p)

        if np.iscomplex(p) or p < 1:
            raise ValueError('p must be at least 1 and real')

        pn = np.sum(np.absolute(self.x) ** p) ** (1. / p)

        return pn

    def norm1(self):
        r"""
        Calculates the 1-norm of a vector.

        Returns
        -------
        l1 : float
            The 1-norm of the vector.

        Notes
        -----
        The 1-norm of a vector :math:`x` is defined as:

        .. math::

            ||x||_1 = |x_1| + |x_2| + \cdots + |x_n|

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        l1 = np.sum(np.absolute(self.x))

        return l1

    def norminf(self):
        r"""
        Calculates the :math:`\inf` norm of a vector.

        Returns
        -------
        ninf : float
            The :math:`\inf` of the vector.

        Notes
        -----
        The :math:`\inf` norm of a vector :math:`x` is defined as:

        .. math::

            ||x||_\inf = max_{1 \leq i \leq n} |x_i|

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        ninf = np.max(np.absolute(self.x))

        return ninf

    def norm_neg_inf(self):

        neg_inf = np.min(np.absolute(self.x))

        return neg_inf


class _MatrixNorm(object):
    r"""
    Class containing implementations of matrix norms for front-end function `norm`.

    Attributes
    ----------
    order : string
        Defines the default norm calculation used by the front-end norm function `norm`.
    n : int
        Row-wise length of array passed in initialization of class
    m : int
        Column-wise length of array passed in initialization of class

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Methods
    -------
    frobenius()
        Calculates the Frobenius norm of a matrix.
    norm1()
        Calculates the 1-norm of a matrix.
    norminf()
        Calculates the inf-norm of a matrix.

    Notes
    -----
    Matrix norms are an extension of vector norms to matrices and are used to define a
    measure of distance on the space of a matrix. More specifically, a matrix norm is
    defined as a function :math:`f: \mathbb{R}^{m \times n} \rightarrow \mathbb{R}`. The double bar
    notation used to denote vector norms are also used for matrix norms. The properties
    of a matrix norm are similar to those of a vector norm.

    - :math:`||A|| \geq 0` for any matrix :math:`A \in \mathbb{R}^{m \times n}`
        + :math:`||A|| = 0` if the matrix :math:`A = 0`
    - :math:`||\alpha A|| = |\alpha| ||A||` for a :math:`m \times n` matrix and scalar :math:`\alpha`
    - :math:`||A + B|| \leq ||A|| + ||B||` for :math:`m \times n` matrices :math:`A` and :math:`B`

    References
    ----------
    Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

    """

    def __init__(self, x):
        self.x = _create_array(x)[0]
        self.order = 'frobenius'
        self.n, self.m = self.x.shape

    def frobenius(self):
        r"""
        Calculates the Frobenius norm of a matrix.

        Returns
        -------
        f : float
            The Frobenius norm of a matrix

        Notes
        -----
        The Frobenius norm is one of the most commonly employed matrix norms and is the default
        norm calculation of the front-end function `norm` as designated by the class
        attribute `method`. The Frobenius norm is defined as:

        .. math::

            ||A||_F = \sqrt{\sum_{i=1}^m \sum_{j=1}^m |a_{ij}|^2}

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        f = 0

        for i in np.arange(self.m):
            for j in np.arange(self.n):
                f = f + np.sum(np.power(np.absolute(self.x[i, j]), 2))

        return np.sqrt(f)

    def norm1(self):
        r"""
        Calculates the 1-norm of a matrix.

        Returns
        -------
        v : float
            The 1-norm of the matrix

        Notes
        -----
        The matrix 1-norm is defined as the maximum absolute column sum of a matrix.

        .. math::

            ||A||_1 = \underset{1 \leq j \leq n}{max}\left( \sum^n_{i=1} |a_{ij}| \right)

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        colsums = []
        for i in np.arange(self.m):
            v = np.sum(np.absolute(self.x[:, i]))
            colsums.append(v)

        return np.max(colsums)

    def norminf(self):
        r"""
        Calculates the inf-norm of a matrix.

        Returns
        -------
        v : float
            The inf-norm of the matrix

        Notes
        -----
        The inf-norm of a matrix is defined as the maximum absolute sum of the matrix rows.

        .. math::

            ||A||_\inf = \underset{1 \leq i \leq n}{max} \left(\sum^n_{j=1} |a_{ij}| \right)

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        rowsums = []
        for i in np.arange(self.n):
            v = np.sum(np.absolute(self.x[i, :]))
            rowsums.append(v)

        return np.max(rowsums)
