# encoding=utf8


import numpy as np
from collections import namedtuple
from scipy.stats import t, norm, rankdata

from mathpy._lib import _create_array
from mathpy.stats.summary import var


def ttest(y1, y2=None, mu=None, var_equal=False):
    r"""
    Performs one and two-sample t-tests.

    Parameters
    ----------
    y1
        First sample to test
    y2
        Second sample. Optional
    mu
        Optional, sets the mean for comparison in the one sample t-test. Default 0.
    var_equal
        Optional, default False. If False, Welch's t-test for unequal variance and
        sample sizes is used. If True, equal variance between samples is assumed
        and Student's t-test is used.

    Returns
    -------
    namedtuple
        Namedtuple containing following values:
        t-value
        degrees of freedom
        p-value
        confidence intervals
        sample means

    Notes
    -----
    Welch's t-test is an adaption of Student's t test and is more performant when the
    sample variances and size are unequal. The test still depends on the assumption of
    the underlying population distributions being normally distributed.

    Welch's t test is defined as:

    .. math::

        t = \frac{\bar{X_1} - \bar{X_2}}{\sqrt{\frac{s_{1}^{2}}{N_1} + \frac{s_{2}^{2}}{N_2}}}

    where:

    :math:`\bar{X}` is the sample mean, :math:`s^2` is the sample variance, :math:`n` is the sample size

    If the :code:`var_equal` argument is True, Student's t-test is used, which assumes the two samples
    have equal variance. The t statistic is computed as:

    .. math::

        t = \frac{\bar{X}_1 - \bar{X}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}

    where:

    .. math::

        s_p = \sqrt{\frac{(n_1 - 1)s^2_{X_1} + (n_2 - 1)s^2_{X_2}}{n_1 + n_2 - 2}

    References
    ----------
    Rencher, A. C., & Christensen, W. F. (2012). Methods of multivariate analysis (3rd Edition).

    Student's t-test. (2017, June 20). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Student%27s_t-test&oldid=786562367

    """
    y1 = _create_array(y1)[0]

    n1 = len(y1)
    s1 = var(y1)
    ybar1 = np.mean(y1)

    if y2 is not None:
        y2 = _create_array(y2)[0]
        n2 = len(y2)
        s2 = var(y2)
        ybar2 = np.mean(y2)

        if var_equal is False:
            tval = float((ybar1 - ybar2) / np.sqrt(s1 / n1 + s2 / n2))
        else:
            sp = np.sqrt(((n1 - 1.) * s1 + (n2 - 1.) * s2) / (n1 + n2 - 2.))
            tval = float((ybar1 - ybar2) / (sp * np.sqrt(1. / n1 + 1. / n2)))

    else:
        ybar2, n2, s2 = 0.0, 1.0, 0.0
        if mu is None:
            mu = 0.0

        tval = float((ybar1 - mu) / np.sqrt(s1 / n1))

    dof = degrees_of_freedom(y1, y2)
    pvalue = _student_t_pvalue(np.absolute(tval), dof)
    intervals = _t_conf_int((ybar1, n1, s1), dof=dof, y=(ybar2, n2, s2))

    if y2 is not None:
        tTestResult = namedtuple('tTestResult', ['tvalue', 'dof', 'pvalue', 'confint', 'x_mean', 'y_mean'])

        tt = tTestResult(tvalue=tval, dof=dof, pvalue=pvalue, confint=intervals, x_mean=ybar1, y_mean=ybar2)

    else:
        tTestResult = namedtuple('tTestResult', ['tvalue', 'dof', 'pvalue', 'confint', 'x_mean'])
        tt = tTestResult(tvalue=tval, dof=dof, pvalue=pvalue, confint=intervals, x_mean=ybar1)

    return tt


def mann_whitney(y1, y2, continuity=True):
    r"""
    Performs the nonparametric Mann-Whitney U test of two independent sample groups.

    Parameters
    ----------
    y1
        One-dimensional array-like (Pandas Series or DataFrame, Numpy array, list, or dictionary)
        designating first sample
    y2
        One-dimensional array-like (Pandas Series or DataFrame, Numpy array, list, or dictionary)
        designating second sample to compare to first
    continuity
        Boolean, optional. If True, apply the continuity correction of :math:`\frac{1}{2}` to the
        mean rank.

    Returns
    -------
    namedtuple
        Namedtuple of following entries that contain resulting Mann-Whitney test statistics.
        Mann-Whitney U Test Statistic: The U Statistic of the Mann-Whitney test
        Mean Rank: The mean rank of U statistic
        Sigma: the standard deviation of U
        z-value: The standardized value of U
        p-value: p-value of U statistic compared to critical value

    Notes
    -----
    The Mann-Whitney U test is a nonparametric hypothesis test that tests the null hypothesis that
    there is an equally likely chance that a randomly selected observation from one sample will be
    less than or greater than a randomly selected observation from a second sample. Nonparametric
    methods are so named since they do not rely on the assumption of normality of the data.

    The test statistic in the Mann-Whitney setting is denoted as :math:`U` and is the minimum of
    the summed ranks of the two samples. The null hypothesis is rejected if :math:`U \leq U_0`,
    where :math:`U_0` is found in a table for small sample sizes. For larger sample sizes,
    :math:`U` is approximately normally distributed.

    The test is nonparametric in the sense it uses the ranks of the values rather than the values
    themselves. Therefore, the values are ordered then ranked from 1 (smallest value) to the largest
    value. Ranks of tied values get the mean of the ranks the values would have received. For example,
    for a set of data points :math:`\{4, 7, 7, 8\}` the ranks are :math:`\{1, 2.5, 2.5, 4\}`. The
    :math:`2.5` rank comes from :math:`2 + 3 = 5 / 2`. The ranks are then added for the values for
    both samples. The sum of the ranks for each sample are typically denoted by :math:`R_k` where
    :math:`k` is a sample indicator.

    :math:`U` for the two samples in the test, is given by:

    References
    ----------
    Mann–Whitney U test. (2017, June 20). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Mann%E2%80%93Whitney_U_test&oldid=786593885

    """
    n1, n2 = len(y1), len(y2)

    ranks = np.concatenate((y1, y2))

    ranks = rankdata(ranks, 'average')

    ranks = ranks[:n1]

    n = n1 + n2

    u1 = n1 * n2 + (n1 * (n1 + 1)) / 2. - np.sum(ranks)
    u2 = n1 * n2 - u1

    u = np.minimum(u1, u2)
    mu = (n1 * n2) / 2. + (0.5 * continuity)

    rankcounts = np.unique(ranks, return_counts=True)[1]

    sigma = np.sqrt(((n1 * n2) * (n + 1)) / 12. * (1 - np.sum(rankcounts ** 3 - rankcounts) / float(n ** 3 - n)))
    z = (np.absolute(u - mu)) / sigma
    p = 1-norm.cdf(z)

    MannWhitneyResult = namedtuple('MannWhitneyResult', ['u', 'meanrank', 'sigma', 'zvalue', 'pvalue'])

    mwr = MannWhitneyResult(u=u, meanrank=mu, sigma=sigma, zvalue=z, pvalue=p)

    return mwr


def degrees_of_freedom(y1, y2=None, var_equal=False):
    r"""
    Computes the degrees of freedom of one or two samples.

    Parameters
    ----------
    y1
        First sample to test
    y2
        Second sample. Optional.
    var_equal
        Optional, default False. If False, Welch's t-test for unequal variance and
        sample sizes is used. If True, equal variance between samples is assumed
        and Student's t-test is used.

    Returns
    -------
    float
        the degrees of freedom

    Notes
    -----
    When Welch's t test is used, the Welch-Satterthwaite equation for approximating the degrees
    of freedom should be used and is defined as:

    .. math::

        \large v \approx \frac{\left(\frac{s_{1}^2}{N_1} +
        \frac{s_{2}^2}{N_2}\right)^2}{\frac{\left(\frac{s_1^2}{N_1^{2}}\right)^2}{v_1} +
        \frac{\left(\frac{s_2^2}{N_2^{2}}\right)^2}{v_2}}

    If the two samples are assumed to have equal variance, the degrees of freedoms become simply:

    .. math::

        v = n_1 + n_2 - 2

    In the case of one sample, the degrees of freedom are:

    .. math::

        v = n - 1

    References
    ----------
    Rencher, A. C., & Christensen, W. F. (2012). Methods of multivariate analysis (3rd Edition).

    Welch's t-test. (2017, June 16). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Welch%27s_t-test&oldid=785961228

    """
    y1 = _create_array(y1)[0]
    n1 = len(y1)
    s1 = var(y1)
    v1 = n1 - 1

    if y2 is not None:
        y2 = _create_array(y2)[0]
        n2 = len(y2)
        s2 = var(y2)
        v2 = n2 - 1

        if var_equal is False:
            v = np.power((s1 / n1 + s2 / n2), 2) / (np.power((s1 / n1), 2) / v1 + np.power((s2 / n2), 2) / v2)
        else:
            v = n1 + n2 - 2

    else:
        v = v1

    return float(v)


def _t_conf_int(x, dof, y=None):

    xbar, xn, xvar = x[0], x[1], x[2]

    if y is not None:
        ybar, yn, yvar = y[0], y[1], y[2]

        low_interval = (xbar - ybar) + t.ppf(0.025, dof) * np.sqrt(xvar / xn + yvar / yn)
        high_interval = (xbar - ybar) - t.ppf(0.025, dof) * np.sqrt(xvar / xn + yvar / yn)
    else:
        low_interval = xbar + 1.96 * np.sqrt((xbar * (1 - xbar)) / xn)
        high_interval = xbar - 1.96 * np.sqrt((xbar * (1 - xbar)) / xn)

    return float(low_interval), float(high_interval)


def _student_t_pvalue(n, dof, test='two-tail'):
    p = (1. - t.cdf(n, dof))

    if test == 'two-tail':
        p *= 2.

    return p
