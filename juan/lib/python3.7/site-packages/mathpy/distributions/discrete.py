# encoding=utf8

r"""

Module containing classes and class methods related to discrete distributions.

"""

import numpy as np

from mathpy.combinatorics.binomial import binom_coeff
from mathpy.random.sample import bernoulli, binomial


class Bernoulli(object):
    r"""
    A Bernoulli discrete random variable. The Bernoulli distribution is the probability
    distribution of Bernoulli trials ('Success/Failure', 'True/False', etc.).

    Attributes
    ----------
    p
        The probability of success of the Bernoulli trial
    q
        The probability of failure of the Bernoulli trial. Equal to :math:`1 - p`

    Methods
    -------
    pmf(k)
        Estimates the probability mass function (probability distribution function of a
        discrete distribution) given probability of success :math:`p` and support
        :math:`k \in [0, 1]`.
    cdf(k)
        Estimates the cumulative distribution function given probability of success :math:`p`
        and support :math:`k \in [0, 1]`.
    mean()
        Calculates the mean of the Bernoulli distribution, which is equivalent to the probability
        of success :math:`p`. The mean is also known as the first moment.
    median()
        Calculates the median of the Bernoulli distribution.
    mode()
        Computes the mode of the Bernoulli distribution.
    variance()
        Method for determining the variance, also known as the second moment, of the Bernoulli
        distribution.
    skewness()
        Returns the skewness (third moment) of the Bernoulli distribution.
    kurtosis()
        Calculates the kurtosis (fourth moment) of the Bernoulli distribution.
    entropy()
        Computes the entropy of the Bernoulli distribution.
    sample(n)
        Draws n random samples from the Bernoulli distribution with given the parameter :math:`p`.

    Notes
    -----
    Please see the individual method documentation for more information on each method.

    References
    ----------
    Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

    Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
        Aberdeen, MD. Army Research Lab.

    Weisstein, Eric W. "Bernoulli Distribution." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/BernoulliDistribution.html

    """
    def __init__(self, p=0.5):
        r"""
        Initializes the Bernoulli class.

        Parameters
        ----------
        p : float, default 0.5
            The probability of success of the Bernoulli trial. Must be between 0 and 1.

        """
        if p < 0 or p > 1:
            raise ValueError('p must be between 0 and 1')

        self.p = p
        self.q = 1.0 - self.p

    def pmf(self, k):
        r"""
        Computes the Bernoulli distribution probability mass function given the
        probability of success :math:`p` and the support :math:`k`, where :math:`k \in [0, 1]`

        Parameters
        ----------
        k : float
            The value of the random variate having a Bernoulli distribution.

        Returns
        -------
        float
            The probability mass function with probability of success :math:`p` and random
            variate :math:`k`.

        Notes
        -----
        The Bernoulli distribution probability mass function is defined as:

        .. math::

            f(k) = \begin{cases}
                1 - p & \text{if}\ 0 \\
                p & \text{if}\ 0
                \end{cases}

        Examples
        --------
        >>> Bernoulli().pmf(0.5)
        0.0
        >>> Bernoulli(0.75).pmf(1)
        0.75
        >>> b = Bernoulli(0.25)
        >>> b.pmf(0)
        0.75

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Weisstein, Eric W. "Bernoulli Distribution." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BernoulliDistribution.html

        """
        if k == 0:
            p = 1.0 - self.p

        elif k == 1:
            p = self.p
        else:
            p = 0.0

        return p

    def cdf(self, k):
        r"""
        Estimates the Bernoulli distribution cumulative distribution function.

        Parameters
        ----------
        k : float
            The value of the random variate having a Bernoulli distribution.

        Returns
        -------
        float
            The probability mass function with probability of success :math:`p` and random
            variate :math:`k`.

        Notes
        -----
        The Bernoulli distribution cumulative distribution function is defined as:

        .. math::

            F(k) = \begin{cases}
                1 - p & \text{if}\ 0 \leq k < 1 \\
                p & \text{if}\ 1
                \end{cases}

        Examples
        --------
        >>> Bernoulli(0.75).cdf(1)
        1.0
        >>> Bernoulli(0.25).cdf(0)
        0.75

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Weisstein, Eric W. "Bernoulli Distribution." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BernoulliDistribution.html

        """
        if k < 0:
            c = 0.0
        elif 0 <= k < 1:
            c = 1.0 - self.p
        else:
            c = 1.0

        return c

    def mean(self):
        r"""
        Computes the mean of the Bernoulli distribution given the probability of success :math:`p`.

        Returns
        -------
        float
            The mean of the Bernoulli distribution with parameter :math:`p`.

        Notes
        -----
        The mean of the Bernoulli distribution given parameter :math:`p` is simply :math:`p`.

        Examples
        --------
        >>> Bernoulli(0.25).mean()
        0.25
        >>> Bernoulli(0.25 * 4).mean()
        1.0

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return self.p

    def median(self):
        r"""
        Calculates the median of the Bernoulli distribution given parameter :math:`p`.

        Returns
        -------
        float
            The median of the Bernoulli distribution.

        Notes
        -----
        The median of the Bernoulli distribution with probability of success :math:`p` is defined as:

        .. math::

            \begin{cases}
                0 & \text{if}\ q > p \\
                0.5 & \text{if}\ q = p \\
                1 & \text{if}\ q < p
            \end{cases}

        Where :math:`q = 1 - p`.

        Examples
        --------
        >>> Bernoulli().median()
        0.5
        >>> Bernoulli(1).median()
        1.0
        >>> Bernoulli(0.25).median()
        0.0

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        if self.q > self.p:
            m = 0.0
        elif self.q == self.p:
            m = 0.5
        else:
            m = 1.0

        return m

    def mode(self):
        r"""
        Returns the mode of the Bernoulli distribution.

        Returns
        -------
        float or tuple
            The mode of the Bernoulli distribution. If :math:`q = p`, where :math:`q = 1 - p`, then the
            tuple :code:`(0, 1)` is returned.

        Notes
        -----
        The mode of the Bernoulli distribution with probability of success :math:`p` is defined as:

        .. math::

            \begin{cases}
                0 & \text{if}\ p < \frac{1}{2} \\
                (0, 1) & \text{if}\ \frac{1}{2} \\
                1 & \text{if}\ p > \frac{1}{2}
            \end{cases}

        Examples
        --------
        >>> Bernoulli().mode()
        (0.0, 1.0)
        >>> Bernoulli(0.51).mode()
        1.0
        >>> Bernoulli(0.49).mode()
        0.0

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        if self.q > self.p:
            m = 0.0
        elif self.q == self.p:
            m = (0.0, 1.0)
        else:
            m = 1.0

        return m

    def variance(self):
        r"""
        Computes the variance of the Bernoulli distribution.

        Returns
        -------
        float
            The computed variance of the Bernoulli distribution

        Notes
        -----
        The variance of the Bernoulli distribution is defined as:

        .. math::

            pq \qquad \text{where}\ q = 1 - p

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return self.p * self.q

    def skewness(self):
        r"""
        Returns the skewness of the Bernoulli distribution.

        Returns
        -------
        float
            The skewness of the distribution.

        Notes
        -----
        The skewness of the Bernoulli is calculated as:

        .. math::

            \frac{1 - 2p}{\sqrt{pq}}

        Examples
        --------
        >>> Bernoulli().skewness()
        0.0
        >>> Bernoulli(.495).skewness()
        0.020001000075006267

        References
        ----------
        Bernoulli distribution. (2017, July 8). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Bernoulli_distribution&oldid=789642547

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        if self.p == 0 or self.p == 1:
            return np.nan

        return (1.0 - 2.0 * self.p) / np.sqrt(self.p * self.q)

    def kurtosis(self):
        r"""
        Computes the kurtosis of the Bernoulli distribution.

        Returns
        -------
        float or nan
            The kurtosis of the Bernoulli distribution. If :math:`p` is 0 or 1, nan is returned.

        Notes
        -----
        The kurtosis of the Bernoulli distribution is defined as:

        .. math::

            \frac{1 - 6pq}{pq}

        Examples
        --------
        >>> Bernoulli().kurtosis()
        -2.0
        >>> Bernoulli(1).kurtosis()
        nan

        References
        ----------
        Bernoulli distribution. (2017, July 8). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Bernoulli_distribution&oldid=789642547

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        if self.p == 0 or self.p == 1:
            return np.nan

        return (1.0 - 6.0 * self.p * self.q) / (self.p * self.q)

    def entropy(self):
        r"""
        Calculates the entropy of the Bernoulli distribution

        Returns
        -------
        float or nan
            The entropy of the Bernoulli distribution. If :math:`p` is 0 or 1, nan is returned.

        Notes
        -----
        The entropy of the Bernoulli distribution is defined as:

        .. math::

            -q \space ln(q) - p \space ln(p)

        The Bernoulli distribution achieves its most entropic value when :math:`p = 0.5`.

        Examples
        --------
        >>> Bernoulli().entropy()
        0.69314718055994529
        >>> Bernoulli(0).entropy()
        nan

        References
        ----------
        Bernoulli distribution. (2017, July 8). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Bernoulli_distribution&oldid=789642547

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        if self.p == 1 or self.p == 0:
            return np.nan

        return -self.q * np.log(self.q) - self.p * np.log(self.p)

    def sample(self, n):
        r"""
        Draws :math:`n` random samples from the Bernoulli distribution.

        Parameters
        ----------
        n : int
            The number of samples to draw

        Returns
        -------
        list
            List of :math:`n` drawn random Bernoulli distribution samples.

        Notes
        -----
        The :code:`sample()` method is simply a wrapper for the :code:`bernoulli()`
        function for generating random samples in the :code:`mathpy.random` module.

        See Also
        --------
        bernoulli()
            Function for generating random samples from the Bernoulli distribution.

        References
        ----------
        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return bernoulli(self.p, n)


class Binomial(object):
    r"""
    Class object representing a binomial discrete random variable. The binomial distribution
    is the discrete probability distribution of the number of successes in a sequence of
    :math:`n` Bernoulli trials. When n = 1, the binomial distribution reduces to the
    Bernoulli distribution.

    Attributes
    ----------
    p : float, default 0.5
            The probability of success of n Bernoulli trials. Must be between 0 and 1.
    n : int, default 10
        The number of Bernoulli trials

    Methods
    -------
    pmf(k, loc=0)
        Estimates the probability mass function of the binomial distribution
    cdf(k, loc=0)
        Estimates the cumulative density function of the binomial distribution
    mean()
        Calculates the mean of the binomial distribution
    variance()
        Computes the variance of the binomial distribution
    skewness()
        Returns the skewness of the binomial distribution
    kurtosis()
        Computes the kurtosis of the binomial distribution
    sample(n)
        Draw n random samples from the binomial distribution

    Notes
    -----
    Please see the individual method documentation for more information on each method.

    References
    ----------
    Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

    Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
        Aberdeen, MD. Army Research Lab.

    Weisstein, Eric W. "Binomial Distribution." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/BinomialDistribution.html

    Binomial distribution. (2017, July 24). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Binomial_distribution&oldid=792108102

    """
    def __init__(self, p=0.5, n=10):
        r"""
        Initializes the Binomial class.

        Parameters
        ----------
        p : float, default 0.5
            The probability of success of n Bernoulli trials. Must be between 0 and 1.
        n : int, default 10
            The number of Bernoulli trials

        """
        if p < 0 or p > 1:
            raise ValueError('parameter p must be between 0 and 1')
        if n < 0:
            raise ValueError('parameter n must be at least 0')
        if np.floor(n) != n:
            n = np.floor(n)

        self.p = p
        self.n = n

    def pmf(self, k, loc=0):
        r"""
        Estimates the probability mass function of the binomial distribution.

        Parameters
        ----------
        k : int
            Number of successes where :math:`0 \leq k \leq n`
        loc : int or float, default 0
            Optional shift parameter.

        Returns
        -------
        float
            The estimated probability mass function

        Notes
        -----
        The binomial distribution probability mass function is defined as:

        .. math::

            f(k) = \begin{cases}
                \binom{n}{k} p^k (1 - p)^{n - k} & 0 \leq k \leq n \\
                0 & \text{otherwise}\
                \end{cases}

        Examples
        --------
        >>> Binomial().pmf(5)
        5.939138117904505e-23
        >>> Binomial(0.25, 50).pmf(10)
        0.09851840993941763

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Weisstein, Eric W. "Binomial Distribution." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BinomialDistribution.html

        """
        if k > self.n:
            raise ValueError('number of successes cannot be higher than number of trials')

        k -= loc

        return binom_coeff(self.n, k) * self.p ** k * (1 - self.p) ** (self.n - k)

    def cdf(self, k, loc=0):
        r"""
        Estimates the binomial distribution cumulative density function.

        Parameters
        ----------
        k : int
            Number of successes where :math:`0 \leq k \leq n`
        loc : int or float, default 0
            Optional shift parameter.

        Returns
        -------
        float
            The estimated cumulative density function

        Notes
        -----
        The binomial distribution cumulative density function is defined as:

        .. math::

            F(k) = \begin{cases}
                \sum^k_{i=0} \binom(n}{i} p^i (1 - p)^{n-i} & 0 \leq k \leq n \\
                1 & k > n
                \end{cases}

        Examples
        --------
        >>> Binomial(0.2, 50).cdf(10)
        0.58354514598914076
        >>> Binomial(0.5, 20).cdf(10)
        0.58809757232666027

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Weisstein, Eric W. "Binomial Distribution." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/BinomialDistribution.html

        """
        if k > self.n:
            raise ValueError('number of successes cannot be higher than number of trials')

        if self.p == 0:
            return 1.0

        k -= loc

        bc = 0.0
        for i in np.arange(k + 1):
            bc = bc + binom_coeff(self.n, i) * self.p ** i * (1 - self.p) ** (self.n - i)

        return bc

    def mean(self):
        r"""
        Computes the mean of the binomial distribution.

        Returns
        -------
        float
            The mean of the binomial distribution.

        Notes
        -----
        The mean of the binomial distribution is defined as :math:`np`.

        Examples
        --------
        >>> Binomial().mean()
        50.0
        >>> Binomial(0.1, 10).mean()
        1.0

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """

        return self.n * self.p

    def variance(self):
        r"""
        Computes the variance of the binomial distribution.

        Returns
        -------
        float
            The variance of the binomial distribution.

        Notes
        -----
        The variance of the binomial coefficient is defined as :math:`np(1 - p)`.

        Examples
        --------
        >>> Binomial().variance()
        25.0
        >>> Binomial(0.25, 20).variance()
        3.75

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return self.mean() * (1 - self.p)

    def skewness(self):
        r"""
        Calculates the skewness of the binomial distribution

        Returns
        -------
        float
            The skewness of the binomial distribution.

        Notes
        -----
        The skewness of the binomial distribution is defined as:

        .. math::

            \frac{1 - 2p}{\sqrt{np(1 - p)}

        Examples
        --------
        >>> Binomial().skewness()
        0.0
        >>> Binomial(0.25, 10).skewness()
        0.36514837167011072

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return (1 - 2 * self.p) / np.sqrt(self.variance())

    def kurtosis(self):
        r"""
        Computes the kurtosis of the binomial distribution.

        Returns
        -------
        float
            The kurtosis of the binomial distribution.

        Notes
        -----
        The kurtosis of the binomial distribution is defined as:

        .. math::

            \frac{1 - 6p(1 - p)}{\sqrt{np(1 - p)}

        Examples
        --------
        >>> Binomial(0.25, 20).kurtosis()
        -0.03333333333333333
        >>> Binomial().kurtosis()
        -0.02

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return (1 - 6 * self.p * (1 - self.p)) / self.variance()

    def sample(self, n):
        r"""
        Draws n random samples from the binomial distribution.

        Parameters
        ----------
        n : int
            Number of samples to draw

        Returns
        -------
        list
            n-length list of random samples drawn from the binomial distribution.

        Notes
        -----
        The :code:`sample()` method is essentially a wrapper method of the :code:`binomial()`
        function for generating random samples from the binomial distribution in the
        :code:`mathpy.stats.random` module.

        See Also
        --------
        binomial()
            Function for drawing random samples from the binomial distribution.

        """
        return binomial(self.n, self.p, n)

#
# class Hypergeometric(object):
#     r"""
#     Class object representing a hypergeometric random variable. The hypergeometric distribution
#     is a discrete probability distribution that models draws from a container without replacement
#     where the result of each draw is a binary response (pass/fail, yes/no, etc.)
#
#     Methods
#     -------
#
#
#     """
#     def __init__(self, n, N, K):
#         self.n = n
#         self.N = N
#         self.K = K
#         self.k = np.minimum(self.K, self.n)
#         self.p = self.K / self.N
#
#     def pmf(self):
#
#         return (binom_coeff(self.K, self.k) * binom_coeff(self.N - self.K, self.n - self.k)) / \
#                binom_coeff(self.N, self.n)
#
#     def cdf(self):
#         pass
#
#     def mean(self):
#
#         return self.n * self.p
#
#     def variance(self):
#
#         return self.n * self.p * (1 - self.p) * ((self.N - self.n) / (self.N - 1))
#
#     def mode(self):
#
#         return ((self.n + 1) * (self.K + 1)) / (self.N + 2)
#
#     def skewness(self):
#
#         num = (self.N - 2 * self.K) * np.sqrt(self.N - 1) * (self.N - 2 * self.n)
#         denom = np.sqrt(self.n * self.K * (self.N - self.K) * (self.N - self.n)) * (self.N - 2)
#
#         return num / denom
#
#     def kurtosis(self):
#
#         num = ((self.N - 1) * self.N ** 2 * (self.N * (self.N + 1) - 6 * self.K * (self.N - self.K) - 6 * self.n * (
#         self.N - self.n)) + 6 * self.n * self.K * (self.N - self.K) * (self.N - self.n) * (5 * self.N - 6))
#
#         denom = self.n * self.K * (self.N - self.K) * (self.N - self.n) * (self.N - 2) * (self.N - 3)
#
#         return num / denom
#
#     def sample(self):
#         pass