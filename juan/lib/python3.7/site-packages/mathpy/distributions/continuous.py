# encoding=utf8

r"""

Module containing classes and class methods related to continuous distributions.

"""

import numpy as np
from mathpy.random.sample import continuous_uniform


class Uniform(object):
    r"""
    A uniform continous random variable. A continous uniform distribution has constant
    probability over its support parameters :math:`a` and :math`b`, which denote the
    distribution's minimum and maximum values, respectively.

    Attributes
    ----------
    a : int or float, default 0.0
        The first parameter, :math:`a`, the minimum value of the uniform distribution.
    b : int or float, default 1.0
        The second parameter, :math:`b`, the maximum value of the uniform distribution.

    Methods
    -------
    pdf(x)
        Estimates the probability density function of the uniform distribution given the
        distribution's parameters :math:`a` and :math:`b`.
    cdf(x)
        Estimates the cumulative density function of the uniform distribution given the
        distribution's parameters :math:`a` and :math:`b`.
    median()
        Compute the median of the distribution.
    mode()
        The mode of the uniform distribution does not uniquely exist, so this method
        simply returns a string saying the mode does not exist.
    mean()
        Calculate the mean, also known as the first moment, of the uniform distribution.
    variance()
        Finds the variance of the uniform distribution. The variance is also know as the
        second moment.
    skew()
        Computes the skewness of the distribution, also known as the third moment.
    kurtosis()
        Calculates the kurtosis of the distribution. Kurtosis is also known as the fourth
        moment.
    entropy()
        Calculates the entropy of the uniform distribution.
    sample(n)
        Draw random samples from the uniform distribution.

    Notes
    -----
    Please see the individual method documentation for more information on each method.

    References
    ----------
    Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
        Boca Raton, Fla.: Chapman & Hall/CRC.

    Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
        Aberdeen, MD. Army Research Lab.

    Weisstein, Eric W. "Uniform Distribution." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/UniformDistribution.html

    """
    def __init__(self, a=0.0, b=1.0):
        r"""
        Initializes the Uniform class.

        Parameters
        ----------
        a : int or float, default 0.0
            Lower bound of the uniform distribution
        b : int or float, default 1.0
            Upper bound of the uniform distribution

        """
        if a > b:
            raise ValueError('parameter b must be greater than a')

        self.a = a
        self.b = b

    def pdf(self, x):
        r"""
        Computes the probability density function of the uniform distribution.

        Parameters
        ----------
        x : int or float
            Value at which to compute the probability density function.

        Returns
        -------
        The estimated probability density function evaluated at the given point.

        Notes
        -----
        The probability density function for a continuous uniform distribution on
        an interval :math:`[a, b]` is defined as:

        .. math::

            P(x) = f(x; a, b) = \begin{cases}
                0 & \text{for}\ x < a \\
                \frac{1}{b - a} & \text{for}\ a \leq x \leq b \\
                0 & \text{for}\ x > b
                \end{cases}

        Examples
        --------
        >>> Uniform().pdf(0.5) # Using default values a=0.0, b=1.0
        1.0
        >>> u = Uniform(5, 10)
        >>> u.pdf(6)
        0.2
        >>> u.pdf(4)
        0

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Weisstein, Eric W. "Uniform Distribution." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/UniformDistribution.html

        """
        if x < self.a or x > self.b:
            return 0.0

        return 1. / (self.b - self.a)

    def cdf(self, x):
        r"""
        Computes the cumulative density function of the uniform distribution.

        Parameters
        ----------
        x : int or float
            Value at which to compute the probability density function.

        Returns
        -------
        The estimated cumulative density function evaluated at the given point.

        Notes
        -----
        The cumulative distribution function of the uniform distribution on the
        interval :math:`[a, b]` is defined as:

        .. math::

            D(x) = F(x|a,b) = \begin{cases}
                0 & \text{for}\ x < a \\
                \frac{x - a}{x - b} & \text{for}\ a \leq x \leq b \\
                1 & \text{for}\ x > b
                \end{cases}

        Examples
        --------
        >>> Uniform().cdf(0.5)
        0.5
        >>> u = Uniform(5, 7)
        >>> u.cdf(7.5)
        0.75
        >>> Uniform().cdf(2)
        0

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Weisstein, Eric W. "Uniform Distribution." From MathWorld--A Wolfram Web Resource.
            http://mathworld.wolfram.com/UniformDistribution.html

        """
        if x < self.a:
            return 0.0
        elif x >= self.b:
            return 1.0
        else:
            return (x - self.a) / (self.b - self.a)

    def median(self):
        r"""
        Computes the median of the uniform distribution over the interval :math:`[a, b]`

        Returns
        -------
        The median of the uniform distribution over the interval :math:`[a, b]`

        Notes
        -----
        The median of the uniform distribution over an interval :math:`[a, b]` is the same as the
        mean of the uniform distribution:

        .. math::

            \frac{a + b}{2}

        Examples
        --------
        >>> Uniform().median()
        0.5
        >>> Uniform(5, 7).median()
        6

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """

        return (self.a + self.b) / 2.

    def mean(self):
        r"""
        Computes the mean of the uniform distribution over the interval :math:`[a, b]`

        Returns
        -------
        The mean of the uniform distribution over the interval :math:`[a, b]`

        Notes
        -----
        The mean of the uniform distribution over an interval :math:`[a, b]` is the same as the
        median of the uniform distribution:

        .. math::

            \frac{a + b}{2}

        Examples
        --------
        >>> Uniform().mean()
        0.5
        >>> Uniform(5, 7).mean()
        6

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return (self.a + self.b) / 2.

    def variance(self):
        r"""
        Computes the variance of the uniform distribution over the interval :math:`[a, b]`.

        Returns
        -------
        The variance of the uniform distribution over the interval :math:`[a, b]`

        Notes
        -----
        The variance of the uniform distribution over an interval :math:`[a, b]` is defined as:

        .. math::

            \frac{(b - a)^2}{12}

        Examples
        --------
        >>> Uniform().variance() # Default interval a = 0.0, b = 1.0
        0.08333333333333333
        >>> u = Uniform(5, 7)
        >>> u.variance()
        0.3333333333333333

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        """
        return (self.b - self.a) ** 2 / 12.

    def entropy(self):
        r"""
        Calculates the entropy (measure of unpredictablility or its average information content)
        over the interval :math:`[a, b]`.

        Returns
        -------
        The entropic value of the uniform distribution over the interval :math:`[a, b]`.

        Notes
        -----
        The entropy of the uniform distribution over the interval :math:`[a, b]` is defined as:

        .. math::

            log(b - a)

        Examples
        --------
        >>> Uniform().entropy()
        0.0
        >>> u = Uniform(5, 7)
        >>> u.entropy()
        0.3010299956639812

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.).
            Aberdeen, MD. Army Research Lab.

        Uniform distribution (continuous). (2017, July 12). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Uniform_distribution_(continuous)&oldid=790192990

        """
        return np.log10(self.b - self.a)

    def sample(self, n):
        r"""
        Draws random samples from the uniform distribution over the interval :math:`[a, b]`.

        Parameters
        ----------
        n : int
            Number of random samples to draw

        Returns
        -------
        list
            n drawn samples from the uniform distribution over the interval :math:`[a, b]`.

        Notes
        -----
        The :code:`sample()` method is simply wraps the :code:`uniform()` random sampling function
        from :code:`mathpy.random`.

        See Also
        --------
        uniform()
            Function used to draw random samples from the uniform distribution.

        """
        return continuous_uniform(self.a, self.b, n)

    @staticmethod
    def mode():
        r"""
        The mode of a uniform distribution does not uniquely exist. This method simply returns a
        string with this statement.

        Returns
        -------
        str

        """
        return 'Mode does not uniquely exist for uniform distribution'

    @staticmethod
    def skewness():
        r"""
        The skewness of the uniform distribution is 0.

        Returns
        -------
        int
            0

        References
        ----------
        Uniform distribution (continuous). (2017, July 12). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Uniform_distribution_(continuous)&oldid=790192990

        """
        return 0.0

    @staticmethod
    def kurtosis():
        r"""
        Returns the kurtosis (-6/5) of the uniform distribution.

        Returns
        -------
        float

        References
        ----------
        Krishnamoorthy, K. (2006). Handbook of statistical distributions with applications.
            Boca Raton, Fla.: Chapman & Hall/CRC.

        Uniform distribution (continuous). (2017, July 12). In Wikipedia, The Free Encyclopedia.
            From https://en.wikipedia.org/w/index.php?title=Uniform_distribution_(continuous)&oldid=790192990

        """
        return -6 / 5
