

import numpy as np
from collections import namedtuple

import mathpy.stats.summary
from mathpy.stats.summary import corr, covar
from mathpy._lib import _create_array


def fa(x, factors=2, rotate=None, covar=False, method=None):
    r"""
    Performs factor analysis of given observation vectors. Acts as a
    front-end to the FactorAnalysis class.

    Parameters
    ----------
    x : array-like
        Numpy ndarray, pandas DataFrame, list of lists or dictionary (keys are column
        names and corresponding values are the column values) representing observation
        vectors
    factors : int, default 2
        The hypothetical number of factors to fit.
    rotate : str
        Specifies the type of rotation to perform on factor loadings. Currently not used.
    covar : boolean, default False
        Determines whether the covariance or correlation matrix of x is used in performing
        factor analysis.
    method : {'principal_component', 'principal_factor', 'iterated_principal_factor'}
        Specifies the factor analysis algorithm. Default is the principal component method.

    Returns
    -------
    namedtuple
        The factor analysis results are collected into a namedtuple with the following values:
        Factor Loadings
        Communality
        Specific Variance
        Complexity
        Proportion of Loadings
        Proportion of Variance
        Proportion of Variance Explained
        Number of Iterations (if the method is 'iterated_principal_factor'

    """
    x = _FactorAnalysis(x, factors, rotate, covar)

    if method is None:
        v = getattr(x, x.method, None)
    else:
        if hasattr(x, method):
            v = getattr(x, method, x.method)
        else:
            return 'no method with name ' + str(method)

    return v()


class _FactorAnalysis(object):
    r"""
    Class containing several algorithms for performing factor analysis.

    Attributes
    ----------
    method : str
        The default algorithm to use when performing factor analysis

    Methods
    -------
    principal_component()
    principal_factor()
    iterated_principal_factor()
    _compute_factors(s)
    _compute_proportions(loadings, eigvals)
    _return_fa_dict(loadings, h2, u2, com, proportion_loadings, var_proportion, exp_proportion, iterations=None)

    Notes
    -----
    Factor analysis is a controversial technique that represents the variables of a dataset
    :math:`y_1, y_2, \cdots, y_p` as linearly related to random, unobservable variables
    called factors, denoted :math:`f_1, f_2, \cdots, f_m$ where $(m < p)`. The factors are
    representative of 'latent variables' underlying the original variables. The existence of
    the factors is hypothetical as they cannot be measured or observed.

    The goal of factor analysis, similar to principal component analysis, is to reduce the
    original variables into a smaller number of factors that allows for easier interpretation.
    For the variables in any of the observation vectors in a sample, the model
    is defined as:

    .. math::

        y_1 - \mu_1 = \lambda_{11} f_1 + \lambda_{12} f_2 + \cdots + \lambda_{1m} f_m + \epsilon_1
        y_2 - \mu_2 = \lambda_{21} f_1 + \lambda_{22} f_2 + \cdots + \lambda_{2m} f_m + \epsilon_2
        \vdots
        y_p - \mu_p = \lambda_{p1} f_1 + \lambda_{p2} f_2 + \cdots + \lambda_{pm} f_m + \epsilon_p

    Where :math:`\mu` is the mean vector and $\epsilon$ is a random error term to show the
    relationship between the factors is not exact. There are several assumptions that must be
    made regarding the relationships of the factor model described above.

    Assume the unobservable factors (latent variables) are independent of each other and of the
    error terms. For the factors :math:`j = 1, 2, \cdots, m`, the expected value of the
    :math:`j`th factor is :math:`0`, :math:`E(f_j) = 0`. The variance of the factor model is
    :math:`1`, :math:`var(f_j) = 1`, and the covariance of two factor models :math:`f_j` and
    :math:`f_k` is :math:`0`, :math:`cov(f_j, f_k) = 0` where :math:`j \neq k`.

    Assume the error terms :math:`\epsilon_i` are independent of each other. Thus, :math:`E(\epsilon) = 0`,
    :math:`var(\epsilon_i) = \psi_i`, and :math:`cov(\epsilon_i, \epsilon_j) = 0`.

    The covariance of the error terms :math:`\epsilon_i` and the factor :math:`f_j` is :math:`0`,
    :math:`cov(\epsilon_i, f_j) = 0`.

    Note the assumption :math:`cov(\epsilon_i, \epsilon_j) = 0` implies the factors represent all
    correlations among the observation vectors :math:`y`. Thus another difference that separates
    PCA and factor analysis is that factor analysis accounts for the covariances of correlations
    among the variables while PCA explains the total variance. With the assumptions made above,
    the variance of :math:`y_i` can be expressed as:

    .. math::

        var(y_i) = \lambda^2_{i1} + \lambda^2_{i2} + \cdots + \lambda^2_{im} + \psi_i

    Expressed more compactly in matrix notation:

    .. math::

        y - \mu = \Lambda f + \epsilon

    We therefore have a partitioning of the variance of the observation vector :math:`y_i` into a
    component due to the common factors, which is called the communality and another called the
    specific variance. Communality is also referred to as common variance and :math:`\psi_i` is
    also known as specificity, unique or residual variance. The factors are grouped into a new
    term denoting the communality, :math:`h^2_i`, with the error term :math:`\psi_i` representing
    the specific variance:

    .. math::

        var(y_i) = (\lambda^2_{i1} + \lambda^2_{i2} + \cdots + \lambda^2_{im}) + \psi_i = h^2_i + \psi_i

    Which is the communality plus the specific variance.

    It must be noted that factor analysis can fail to fit the data; however, a failed fit can indicate
    that it is not known how many factors there should be and what the factors are.

    References
    ----------
    Rencher, A. (2002). Methods of Multivariate Analysis (2nd ed.). Brigham Young University: John Wiley & Sons, Inc.

    """
    def __init__(self, x, factors=None, rotate=None, covar=False):
        r"""
        Initializes the FactorAnalysis class.

        Parameters
        ----------
        x : array-like
            Numpy ndarray, pandas DataFrame, list of lists or dictionary (keys are column
            names and corresponding values are the column values) representing observation
            vectors
        factors : int, default None
            Number of underlying hypothetical factors
        rotate : str, default None
            Rotation to use when performing the factor analysis. Currently not used.
        covar : boolean, default False
            If False (default), perform the factor analysis using the covariance matrix. If
            True, the factor analysis is computed with the correlation matrix. It is highly
            recommended to use the correlation matrix in the vast majority of cases as
            variables with comparatively large variances can dominate the diagonal of the
            covariance matrix and the factors.

        """
        self.x = _create_array(x)[0]
        self.factors = int(factors)

        if self.factors > self.x.shape[1]:
            raise ValueError('number of factors cannot exceed number of observation vectors')

        self.rotate = rotate
        self.covar = covar
        self.method = 'principal_component'

    def principal_component(self):
        r"""
        Performs factor analysis using the principal component method

        Returns
        -------
        namedtuple
            The factor analysis results are collected into a namedtuple with the following values:
            Factor Loadings
            Communality
            Specific Variance
            Complexity
            Proportion of Loadings
            Proportion of Variance
            Proportion of Variance Explained

        Notes
        -----
        The principal component method is rather misleading in its naming it that no principal
        components are calculated. The approach of the principal component method is to
        calculate the sample covariance matrix :math:`S` from a sample of data and then find an estimator,
        denoted :math:`\hat{\Lambda}` that can be used to factor :math:`S`.

        .. math::

            S = \hat{\Lambda} \hat{\Lambda}'

        Another term, :math:`\Psi`, is added to the estimate of :math:`S`, making the above
        :math:`S = \hat{\Lambda} \hat{\Lambda}' + \hat{\Psi}`. :math:`\hat{\Psi}` is a diagonal
        matrix of the specific variances :math:`(\hat{\psi_1}, \hat{\psi_2}, \cdots, \hat{\psi_p})`.
        :math:`\Psi` is estimated in other approaches to factor analysis such as the principal
        factor method and its iterated version but is excluded in the principal component method
        of factor analysis. The reason for the term's exclusion is since $\hat{\Psi}$ equals the
        specific variances of the variables, it models the diagonal of :math:`S` exactly.

        Spectral decomposition is employed to factor :math:`S` into:

        .. math::

            S = CDC'

        Where :math:`C` is an orthogonal matrix of the normalized eigenvectors of :math:`S` as
        columns and :math:`D` is a diagonal matrix with the diagonal equaling the eigenvalues
        of :math:`S`. Recall that all covariance matrices are positive semidefinite. Thus the
        eigenvalues must be either positive or zero which allows us to factor the diagonal matrix
        :math:`D` into:

        .. math::

            D = D^{1/2} D^{1/2}

        The above factor of :math:`D` is substituted into the decomposition of :math:`S`.

        .. math::

            S = CDC' = C D^{1/2} D^{1/2} C'

        Then rearranging:

        .. math::

            S = (CD^{1/2})(CD^{1/2})'

        Which yields the form :math:`S = \hat{\Lambda} \hat{\Lambda}'`. Since we are interested
        in finding :math:`m` factors in the data, we want to find a :math:`\hat{\Lambda}` that
        is :math:`p \times m` with :math:`m` smaller than :math:`p`. Thus :math:`D` can be
        defined as a diagonal matrix with :math:`m` eigenvalues (making it :math:`m \times m`) on
        the diagonal and :math:`C` is therefore :math:`p \times m` with the corresponding eigenvectors,
        which makes :math:`\hat{\Lambda} p \times m`.

        Note if the correlation matrix is used rather than the covariance matrix, there is no need
        to decompose the matrix in order to compute the eigenvalues and eigenvectors as correlation
        matrices are inherently positive semidefinite.

        References
        ----------
        Rencher, A. (2002). Methods of Multivariate Analysis (2nd ed.).
            Brigham Young University: John Wiley & Sons, Inc.

        """
        if self.covar is True:
            s = covar(self.x)
        else:
            s = corr(self.x)

        eigvals, loadings, h2, u2, com = self._compute_factors(s)

        proportion_loadings, var_proportion, exp_proportion = self._compute_proportions(loadings, eigvals)

        return self._return_fa_stats(loadings, h2, u2, com, proportion_loadings, var_proportion, exp_proportion)

    def principal_factor(self):
        r"""
        Calculates the factor analysis with the principal factor (principal axis) method.

        Returns
        -------
        namedtuple
            The factor analysis results are collected into a namedtuple with the following values:
            Factor Loadings
            Communality
            Specific Variance
            Complexity
            Proportion of Loadings
            Proportion of Variance
            Proportion of Variance Explained

        Notes
        -----
        The principal factor method of factor analysis (also called the principal axis method)
        finds an initial estimate of :math:`\hat{\Psi}` and factors :math:`S - \hat{\Psi}`, or
        :math:`R - \hat{\Psi}` for the correlation matrix. Rearranging the estimated covariance
        and correlation matrices with the estimated :math:`p \times m` :math:`\hat{\Lambda}` matrix yields:

        .. math::

            S - \hat{\Psi} = \hat{\Lambda} \hat{\Lambda}^\prime
            R - \hat{\Psi} = \hat{\Lambda} \hat{\Lambda}^\prime

        Therefore the principal factor method begins with eigenvalues and eigenvectors of :math:`S - \hat{\Psi}`
        or :math:`R - \hat{\Psi}`. :math:`\hat{\Psi}` is a diagonal matrix of the :math:`i`th communality.
        As in the principal component method, the :math:`i`th communality, :math:`\hat{h}^2_i`, is equal to
        :math:`s_{ii} - \hat{\psi}_i` for :math:`S - \hat{\Psi}` and :math:`1 - \hat{\psi}_i` for
        :math:`R - \hat{\Psi}`. The diagonal of :math:`S` or :math:`R` is replaced by their respective
        communalities in :math:`\hat{\psi}_i` which gives us the following forms:

        .. math::

            S - \hat{\Psi} =
            \begin{bmatrix}
              \hat{h}^2_1 & s_{12} & \cdots & s_{1p} \\
              s_{21} & \hat{h}^2_2 & \cdots & s_{2p} \\
              \vdots & \vdots & & \vdots \\
              s_{p1} & s_{p2} & \cdots & \hat{h}^2_p \\
            \end{bmatrix}

            R - \hat{\Psi} =
            \begin{bmatrix}
              \hat{h}^2_1 & r_{12} & \cdots & r_{1p} \\
              r_{21} & \hat{h}^2_2 & \cdots & r_{2p} \\
              \vdots & \vdots & & \vdots \\
              r_{p1} & r_{p2} & \cdots & \hat{h}^2_p \\
            \end{bmatrix}

        An initial estimate of the communalities is made using the squared multiple correlation between
        the observation vector :math:`y_i` and the other :math:`p - 1` variables. The squared multiple
        correlation in the case of :math:`R - \hat{\Psi}` is equivalent to the following:

        .. math::

            \hat{h}^2_i = 1 - \frac{1}{r^{ii}}

        Where :math:`r^{ii}` is the :math:`i`th diagonal element of :math:`R^{-1}`. In the case of
        :math:`S - \hat{\Psi}`, the above is multiplied by the variance of the respective variable.

        The factor loadings are then calculated by finding the eigenvalues and eigenvectors of the
        :math:`R - \hat{\Psi}` or :math:`S - \hat{\Psi}` matrix.

        References
        ----------
        Rencher, A. (2002). Methods of Multivariate Analysis (2nd ed.).
            Brigham Young University: John Wiley & Sons, Inc.

        """
        if self.covar is True:
            s = corr(self.x)
        else:
            s = covar(self.x)

        smc = (1 - 1 / np.diag(np.linalg.inv(s)))

        np.fill_diagonal(s, smc)

        eigvals, loadings, h2, u2, com = self._compute_factors(s)

        proportion_loadings, var_proportion, exp_proportion = self._compute_proportions(loadings, eigvals)

        return self._return_fa_stats(loadings, h2, u2, com, proportion_loadings, var_proportion, exp_proportion)

    def iterated_principal_factor(self):
        r"""
        Performs factor analysis using the iterated principal factor method.

        Returns
        -------
        namedtuple
            The factor analysis results are collected into a namedtuple with the following values:
            Factor Loadings
            Communality
            Specific Variance
            Complexity
            Proportion of Loadings
            Proportion of Variance
            Proportion of Variance Explained
            Number of Iterations

        Notes
        -----
        The iterated principal factor method is an extension of the principal factor method that seeks
        improved estimates of the communality. As in the principal factor method, initial estimates of
        :math:`R - \hat{\Psi}` or :math:`S - \hat{\Psi}` are found to obtain :math:`\hat{\Lambda}` from
        which the factors are computed. In the iterated principal factor method, the initial estimates
        of the communality are used to find new communality estimates from the loadings in
        :math:`\hat{\Lambda}` with the following:

        .. math::

            \hat{h}^2_i = \sum^m_{j=1} \hat{\lambda}^2_{ij}

        The values of :math:`\hat{h}^2_i` are then substituted into the diagonal of :math:`R - \hat{\Psi}`
        or :math:`S - \hat{\Psi}` and a new value of :math:`\hat{\Lambda}` is found. This iteration
        continues until the communality estimates converge, though sometimes convergence does not occur.
        Once the estimates converge, the eigenvalues and eigenvectors are calculated from the iterated
        :math:`R - \hat{\Psi}` or :math:`S - \hat{\Psi}` matrix to arrive at the factor loadings.

        References
        ----------
        Rencher, A. (2002). Methods of Multivariate Analysis (2nd ed.).
            Brigham Young University: John Wiley & Sons, Inc.

        """
        minerr = 0.001
        iterations = []

        if self.covar is True:
            s = covar(self.x)
        else:
            s = corr(self.x)

        smc = (1 - 1 / np.diag(np.linalg.inv(s)))

        np.fill_diagonal(s, smc)

        h2 = np.trace(s)
        err = h2

        while err > minerr:
            eigval, eigvec = np.linalg.eig(s)

            c = eigvec[:, :self.factors]
            d = np.diag(eigval[:self.factors])

            loadings = np.dot(c, np.sqrt(d))

            psi = np.dot(loadings, loadings.T)

            h2_new = np.trace(psi)
            err = np.absolute(h2 - h2_new)
            h2 = h2_new

            iterations.append(h2_new)

            np.fill_diagonal(s, np.diag(psi))

        h2 = np.sum(loadings ** 2, axis=1)

        u2 = 1 - h2

        com = h2 ** 2 / np.sum(loadings ** 4, axis=1)

        proportion_loadings = np.sum(loadings ** 2, axis=0)

        var_proportion, exp_proportion = [], []

        for i in proportion_loadings:
            var_proportion.append(i / np.sum(eigval))
            exp_proportion.append(i / np.sum(proportion_loadings))

        return self._return_fa_stats(loadings, h2, u2, com, proportion_loadings, var_proportion, exp_proportion, iter)

    def _compute_factors(self, s):
        eigval, eigvec = np.linalg.eig(s)

        c = eigvec[:, 0:self.factors]
        d = np.diag(eigval[0:self.factors])

        loadings = np.dot(c, np.sqrt(d))

        h2 = np.sum(loadings ** 2, axis=1)

        u2 = np.diag(s) - h2

        com = h2 ** 2 / np.sum(loadings ** 4, axis=1)

        return eigval, loadings, h2, u2, com

    def _return_fa_stats(self, loadings, h2, u2, com, proportion_loadings, var_proportion, exp_proportion,
                         iterations=None):

        if self.method != 'iterated_principal_factor':
            FactorAnalysis = namedtuple('FactorAnalysis', ['loadings', 'h2', 'u2', 'com', 'proportion_loadings',
                                                           'proportion_variance', 'proportion_explained'])

            f = FactorAnalysis(loadings=loadings, h2=h2, u2=u2, com=com, proportion_loadings=proportion_loadings,
                               proportion_variance=var_proportion, proportion_explained=exp_proportion)

        else:
            FactorAnalysis = namedtuple('FactorAnalysis', ['loadings', 'h2', 'u2', 'com', 'proportion_loadings',
                                                           'proportion_variance', 'proportion_explained', 'iterations'])

            f = FactorAnalysis(loadings=loadings, h2=h2, u2=u2, com=com, proportion_loadings=proportion_loadings,
                               proportion_variance=var_proportion, proportion_explained=exp_proportion,
                               iterations=iterations)

        return f

    @staticmethod
    def _compute_proportions(loadings, eigvals):
        var_proportion, exp_proportion = [], []
        proportion_loadings = np.sum(loadings ** 2, axis=0)

        for i in proportion_loadings:
            var_proportion.append(i / np.sum(eigvals))
            exp_proportion.append(i / np.sum(proportion_loadings))

        return proportion_loadings, var_proportion, exp_proportion
