# encoding=utf8


"""
Module containing front-end function with several
algorithm implementations of QR decomposition defined as methods in
the QR class.

"""


from functools import reduce

import numpy as np
from scipy.linalg import block_diag

from mathpy.linalgebra.norm import norm
from mathpy._lib import _create_array


def qr(x, method=None):
    r"""
    Interface to QR class for performing QR decomposition.
    Several methods are available for computing the QR decomposition,
    including Householder reflections and multiple implementations of
    Gram-Schmidt. Please see the QR class for more on each QR method.

    Parameters
    ----------
    x : array_like
        Accepts a list, nested list, dictionary, pandas DataFrame or
        pandas Series. The private function _create_array is called
        to create a copy of x as a numpy array.
    method : {'householder', 'mgs', 'gramschmidt'}, optional
        Default method for performing QR decomposition is Householder reflections.
        Please refer to the QR class for implementation of these methods.

    Returns
    -------
    qr : tuple
        Returns a tuple containing the orthogonal matrix Q and the upper-triangular
        matrix R resulting from QR decomposition.

    Notes
    -----
    QR decomposition plays an important role in many statistical techniques such as least
    squares estimation. Also called QR factorization, the method is a procedure to decompose
    a matrix :math:`A` into a product :math:`A = QR` where :math:`Q` is an orthogonal
    :math:`m \times n` matrix and :math:`R` is an upper triangular :math:`n \times n` matrix.

    There are several methods to computing the QR decomposition of a matrix, of which the most
    common is utilizing Householder reflections due to its relative speed and numerical stability.
    Other methods include the Modified Gram-Schmidt Orthogonalization process and Givens rotation.

    Examples
    --------
    >>> import pandas as pd
    >>> a = pd.DataFrame({0: [2,2,1], 1: [-2,1,2], 2: [18,0,0]})
    >>> q, r = qr(a)
    >>> q
    array([[-0.66666667,  0.66666667, -0.33333333],
       [-0.66666667, -0.33333333,  0.66666667],
       [-0.33333333, -0.66666667, -0.66666667]])
    >>> r
    array([[ -3.00000000e+00,   2.22044605e-16,  -1.20000000e+01],
       [ -1.16573418e-16,  -3.00000000e+00,   1.20000000e+01],
       [  1.55431223e-16,   5.32907052e-17,  -6.00000000e+00]])
    >>> b = [[1,0,1], [0,1,0]]
    >>> q_b, r_b = qr(b)
    >>> q_b
    array([[-0.70710678,  0.        ],
       [ 0.        , -1.        ],
       [-0.70710678,  0.        ]])
    >>> r_b
    array([[-1.41421356,  0.        ],
       [ 0.        , -1.        ]])

    """

    x = _QR(x)
    if method is None:
        f = getattr(x, x.method, None)
    else:
        try:
            f = getattr(x, method, x.method)
        except ValueError:
            print('no attribute with name ' + str(method))
            raise

    return f()


class _QR(object):
    r"""
    Class containing several implementations for performing QR decomposition.
    These methods include Householder reflections and Modified and Classical
    Gram-Schmidt.

    Parameters
    ----------
    x : array_like
        Accepts a list, nested list, dictionary, pandas DataFrame or
        pandas Series. The private function _create_array is called
        to create a copy of x as a numpy array.

    Methods
    -------
    householder()
        Performs Householder reflection approach to QR decomposition.
    mgs()
        Implements the Modified Gram-Schmidt procedure for performing
        QR decomposition
    gramschmidt()
        Implementation of the Classical Gram-Schmidt procedure

    Notes
    -----
    See specific methods in class for more details on implementations.

    """
    def __init__(self, x):
        self.x = _create_array(x)[0]
        self.m = self.x.shape[0]
        self.n = self.x.shape[1]
        self.r = np.zeros((self.n, self.n))
        self.q = np.zeros((self.m, self.n))
        self.method = 'householder'

    def householder(self):
        r"""
        Implementation of Householder reflections method to performing QR
        decomposition.

        Returns
        -------
        qr : tuple
            Returns a tuple containing the orthogonal matrix Q and the upper-triangular
            matrix R resulting from QR decomposition.

        Notes
        -----
        The Householder reflection approach to QR decomposition is the more common approach
        due to its numerical stability compared to Gram-Schmidt and its relative speed to
        Givens rotations. The orthogonal matrix :math:`Q` is defined as successive Householder
        matrices :math:`H_1 \cdots H_n` while :math:`R` is upper triangular, defined as
        :math:`R = Q^T A`.

        Householder matrices :math:`H` are defined as:

        .. math::

            H = I - 2vv^T

        References
        ----------
        Golub, G., & Van Loan, C. (2013). Matrix computations (3rd ed.). Baltimore (MD): Johns Hopkins U.P.

        Householder transformation. (2017, March 19). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Householder_transformation&oldid=771169379

        Trefethen, L., & Bau, D. (1997). Numerical linear algebra (1st ed.). Philadelphia: SIAM.

        """
        h = []
        r = self.x.copy()

        if self.m > self.n:
            c = self.n
        else:
            c = self.m

        for j in np.arange(c):
            hj = _householder_mat(r[j:self.m, j])
            if j > 0:
                hj = block_diag(np.eye(j), hj)

            r = np.dot(hj, r)
            h.append(hj)

        self.q = reduce(np.dot, reversed(h))[0:self.n].T
        r = np.array(r)[0:self.n]

        qr = (self.q, r)

        return qr

    def mgs(self):
        r"""
        Implementation of the Modified Gram-Schmidt procedure for computing the QR decomposition.
        The modified procedure is more numerically stable than the classic Gram-Schmidt process, but
        is still less stable than the Householder reflection approach.

        Returns
        -------
        qr : tuple
            Returns a tuple containing the orthogonal matrix Q and the upper-triangular
            matrix R resulting from QR decomposition.

        Notes
        -----
        The Modified Gram-Schmidt algorithm for deomposing a matrix into a product of an
        orthogonal matrix :math:`Q` and an upper-triangular matrix :math:`R` is essentially
        a rearrangement of the Classical Gram-Schmidt algorithm that has much more stable
        numerical properties (the resulting matrix :math:`Q` is actually orthogonal).

        References
        ----------
        Gram–Schmidt process. (2017, April 4). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Gram%E2%80%93Schmidt_process&oldid=773752446

        Golub, G., & Van Loan, C. (2013). Matrix computations (1st ed.). Baltimore (MD): Johns Hopkins U.P.

        Trefethen, L., & Bau, D. (1997). Numerical linear algebra (1st ed.). Philadelphia: SIAM.

        """
        for j in np.arange(self.n):
            v = self.x[:, j]

            for i in np.arange(j):
                self.r[i, j] = np.dot(np.transpose(self.q[:, i]), v)
                v = v - self.r[i, j] * self.q[:, i]

            self.r[j, j] = norm(v)
            self.q[:, j] = v / self.r[j, j]

        qr = (self.q, self.r)

        return qr

    def gramschmidt(self):
        r"""
        Implementation of the classic Gram-Schmidt algortihm of QR decomposition. Returns
        the 'thin' QR matrix.

        Returns
        -------
        qr : tuple
            Returns a tuple containing the orthogonal matrix Q and the upper-triangular
            matrix R resulting from QR decomposition.

        Notes
        -----
        The Classical Gram-Schmidt algorithm is another method for computing the :math:`QR`
        decomposition. The classical method has very poor numerical properties which often
        result in a non-orthogonal :math:`q` matrix. Thus, it is not recommended to employ
        the classical method in practice, but is presented here for completeness. For a
        full rank matrix :math:`A`, the :math:`QR` decomposition can be directly computed
        by solving for :math:`q_k`:

        .. math::

            q_k = (a_k - \sum^{k-1}_{i=1} r_{ik}q_i) / r_{kk}

        Where :math:`z_k` is considered a unit 2-norm vector in the direction of :math:`z_k`.

        .. math::

            z_k = a_k - \sum^{k-1}_{i=1} r_{ik} q_i

        References
        ----------
        Gram–Schmidt process. (2017, April 4). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Gram%E2%80%93Schmidt_process&oldid=773752446

        Golub, G., & Van Loan, C. (2013). Matrix computations (1st ed.). Baltimore (MD): Johns Hopkins U.P.

        """
        a = self.x.copy()

        self.r[0,0] = norm(a[:, 0])
        self.q[:, 0] = a[:, 0] / float(self.r[0,0])

        for k in np.arange(1, self.n):
            self.r[:k-1, k] = np.dot(np.transpose(self.q[:self.m, :k-1]), a[:self.m, k])
            z = a[:self.m, k] - np.dot(self.q[:self.m, :k-1], self.r[:k -1, k])
            self.r[k,k] = norm(z)
            self.q[:self.m, k] = z / float(self.r[k,k])

        qr = (self.q, self.r)

        return qr
    # TODO: Complete Reorthogonalization methods for QR decomposition
    # def reorthomgs(self):
    #     for j in np.arange(self.n):
    #         tt = 0
    #         t = norm(self.q[j])
    #         reorth = 1
    #
    #         while reorth:
    #             if j > 1:
    #                 for i in np.arange(j):
    #                     v = np.dot(np.transpose(self.q[i]), self.q[j])
    #                     if tt == 0:
    #                         self.r[i, j] = v
    #                     self.q[j] = self.q[j] - v * self.q[i]
    #
    #             tt = norm(self.q[j])
    #             reorth = 0
    #             if tt < t / 10:
    #                 t = tt
    #                 reorth = 1
    #
    #         self.r[j, j] = tt
    #         self.q[j] = self.q[j] / self.r[j, j]
    #
    #     qr = (self.q, self.r)
    #
    #     return qr
#
#     def reorthomgs2(self):
#         z = []
#         for j in np.arange(self.n):
#             t = norm(self.q[j])
#             nach = 1
#             u = 0
#             while nach:
#                 u += 1
#                 for i in np.arange(j):
#                     s = np.dot(np.transpose(self.q[i]), self.q[j])
#                     self.r[i, j] = self.r[i, j] + s
#                     self.q[j] = self.q[j] - s * self.q[i]
#
#                 tt = norm(self.q[j])
#                 if tt > 10 * np.finfo(float).eps * t & tt < t / 10:
#                     nach = 1
#                     t = tt
#                 else:
#                     nach = 0
#                     if tt < 10 * np.finfo(float).eps * t:
#                         tt = 0
#
#             z.append(u)
#
#             self.r[j, j] = tt
#
#             if tt * np.finfo(float).eps == 0:
#                 tt = 1 / tt
#             else:
#                 tt = 0
#
#             self.q[j] = self.q[j] * tt
#
#         qr = [self.q, self.r]
#
#         return qr

# TODO: Document private function? Keep private?
def _householder_mat(a):
    e = np.append(1, np.repeat(0, len(a) - 1))
    v = np.sign(a[0]) * norm(a) * e + a
    h = np.eye(len(a)) - (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])

    return h
