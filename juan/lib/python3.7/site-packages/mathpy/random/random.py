# encoding=utf8


import numpy as np
from datetime import datetime
from mathpy.numtheory.integers import isrelativelyprime


def lcg(n=10):
    r"""
    Implementation of a linear congruential generator for generating n random samples in U(0, 1).

    Parameters
    ----------
    n : int, default 10
        The number of random samples to generate

    Returns
    -------
    list or float
        If n > 1, a list of the n randomly generated samples is returned. If n = 1,
        the single generated value is returned as a float.

    Notes
    -----
    Linear congruential generators (LCGs) are a class of pseudorandom number generator (PRNG)
    algorithms used for generating sequences of random-like numbers. The generation of random
    numbers plays a large role in many applications ranging from cryptography to Monte Carlo
    methods. Linear congruential generators are one of the oldest and most well-known methods
    for generating random numbers primarily due to their comparative ease of implementation
    and speed and their need for little memory. Other methods such as the Mersenne Twister are
    much more common in practical use today.

    Linear congruential generators are defined by a recurrence relation:

    .. math::

        \large{X_{i+1} = (aX_i + c) \space \text{mod} \space m}

    There are many choices for the parameters :math:`m`, the modulus, :math:`a`, the multiplier,
    and :math:`c` the increment. Wikipedia has a seemingly comprehensive list of the parameters
    in common use here:
    https://en.wikipedia.org/wiki/Linear_congruential_generator#Parameters_in_common_use

    References
    ----------
    Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.). Aberdeen, MD. Army Research Lab.

    """
    r = []

    m = 2 ** 32
    a = 1103515245
    c = 12345

    d = _generate_seed_number()

    for _ in np.arange(n):
        d = (a * d + c) % m
        r.append(d / m)

    if len(r) == 1:
        r = r[0]

    return r


def mcg(n=10):
    r"""
    Implementation of a Lehmer random number generator, also known as a multiplicative congruential
    generator for generating n random samples in U(0, 1).

    Parameters
    ----------
    n : int, default 10
        The number of random samples to generate

    Returns
    -------
    list or float
        If n > 1, a list of the n randomly generated samples is returned. If n = 1,
        the single generated value is returned as a float.

    Notes
    -----
    Multiplicative congruential generators, also known as Lehmer random number generators, is a
    type of linear congruential generator for generating pseudorandom numbers in :math:`U(0, 1)`.
    The multiplicative congruential generator, often abbreviated as MLCG or MCG, is defined as a
    recurrence relation similar to the LCG with :math:`c = 0`.

    .. math::

        X_{i+1} = aX_i \space \text{mod} \space m

    Unlike the LCG, the parameters :math:`a` and :math:`m` for multiplicative congruential generators are more
    restricted and the initial seed :math:`X_0` must be relatively prime to the modulus :math:`m` (the greatest
    common divisor between :math:`X_0` and :math:`m` is :math:`0`). The current parameters in common use are
    :math:`m = 2^{31} - 1 = 2,147,483,647 \text{and} a = 7^5 = 16,807`. However, in a correspondence from
    the Communications of the ACM, Park, Miller and Stockmeyer changed the value of the parameter
    :math:`a`, stating:

    "The minimal standard Lehmer generator we advocated had a modulus of m = 2^31 - 1 and a multiplier of  a = 16807.
    Relative to this particular choice of multiplier, we wrote "... if this paper were to be written again in a few
    years it is quite possible that we would advocate a different multiplier .... " We are now prepared to do so.
    That is, we now advocate a = 48271 and, indeed, have done so "officially" since July 1990. This new advocacy is
    consistent with the discussion on page 1198 of [10]. There is nothing wrong with 16807; we now believe, however,
    that 48271 is a little better (with q = 44488, r = 3399).

    When using a large prime modulus :math:`m` such as :math:`2^{31} - 1`, the multiplicative congruential generator
    can overflow. Schrage's method was invented to overcome the possibility of overflow and is based on the fact that
    :math:`a(m \space \text{mod} \space a) < m`. We can check the parameters in use satisfy this condition:

    Schrage's method restates the modulus :math:`m1` as a decomposition :math:`m = aq + r` where
    :math:`r = m \space \text{mod} \space a` and :math:`q = m / a`.

    .. math::

        ax \space \text{mod} \space m = \begin{cases}
        a(x \space \text{mod} \space q) - r\frac{x}{q} & \text{if} \space x \space \text{is} \geq 0 \\
        a(x \space \text{mod} \space q) - r\frac{x}{q} + m & \text{if} \space x \space \text{is} \leq 0 \end{cases}

    References
    ----------
    Anne Gille-Genest (March 1, 2012).
        Implementation of the Pseudo-Random Number Generators and the Low Discrepancy Sequences.

    Saucier, R. (2000). Computer Generation of Statistical Distributions (1st ed.). Aberdeen, MD. Army Research Lab.

    Stephen K. Park; Keith W. Miller; Paul K. Stockmeyer (1988). "Technical Correspondence".
        Communications of the ACM. 36 (7): 105-110.

    """
    rn = []

    m = 2147483647
    a = 48271  # 16807
    q = 44488  # 127773
    r = 3399  # 2836

    s = _generate_seed_number()

    while isrelativelyprime(s, m) is False:
        s += 1

    for _ in np.arange(n):
        h = s / q
        l = s % q
        t = a * l - r * h
        if t > 0:
            s = t
        else:
            s = t + m

        rn.append(s / m)

    if len(rn) == 1:
        rn = rn[0]

    return rn


def clcg_32bit(n=10):
    r"""
    Implementation of a combined linear congruential generator suited for 32-bit processors as proposed by
    L'Ecuyer.

    Parameters
    ----------
    n : int, default 10
        The number of random samples to generate

    Returns
    -------
    list or float
        If n is greater than 1, a list of the generated random values is returned. If n is equal to 1, the
        generated value is returned as float.

    Notes
    -----
    Combined linear congruential generators are a type of PRNG (pseudorandom number generator) that combine
    two or more LCGs (linear congruential generators). The combination of two or more LCGs into one random
    number generator can result in a marked increase in the period length of the generator which makes them
    better suited for simulating more complex systems. The combined linear congruential generator algorithm is
    defined as:

    .. math::

        X_i \equiv \Bigg(\sum^k_{j=1} (-1)^{j-1} Y_{i,j} \Bigg) \space (\text{mod} \space (m_1 - 1))

    Where :math:`m_1` is the modulus of the LCG, :math:`Y_{i,j}` is the :math:`ith` input from the :math:`jth`
    LCG and :math:`X_i` is the :math:`ith` random generated value.

    L'Ecuyer describes a combined linear generator that utilizes two LCGs in *Efficient and Portable Combined
    Random Number Generators* for 32-bit processors. To be precise, the congruential generators used are
    actually multiplicative since :math:`c_1 = c_2 = 0`. The parameters used for the MCGs are:

    .. math::

        a_1 = 40014 \qquad m_1 = 2147483563 \qquad a_2 = 40692 \qquad m_2 = 2147483399

    The combined linear congruential generator algorithm proposed by L'Ecuyer can be described with the
    following steps:

    The two MCGs, :math:`Y_{0,1}, \space Y_{0,2}`, are seeded. The seed values are recommended to be in the
    range :math:`[1, m_1 - 1]` and :math:`[1, m_2 - 1]`, respectively.

    Next, the two MCGs are evaluated using the algorithm above:

    .. math::

        Y_{i+1,1} = a_1 \times Y_{i,1} (\text{mod} \space m_1) \qquad Y_{i+1,2} = a_1 \times Y_{i,2}
        (\text{mod} \space m_2)

    With :math:`Y_{i+1,1} \text{and} Y_{i+1,2}` evaluated, find :math:`X_{i+1}`

    .. math::

        X_{i+1} = (Y_{i+1,1} - Y_{i+1,2}) \space \text{mod} \space m_1 - 1

    Finally, the random number to be output can be generated:

    .. math::

        R_{i+1} = \begin{cases} \frac{X_{i+1}}{m_1} & \text{for} \space X_{i+1} > 0 \\
        (\frac{X_{i+1}}{m_1}) + 1 & \text{for} \space X_{i+1} < 0 \\
        \frac{(m_1 - 1)}{m_1} & \text{for} \space X_{i+1} = 0 \end{cases}

    The function utilizes the :code:`numpy`'s :code:`randint()` function generate the seeds in the recommended ranges.
    Although there is nothing drastically wrong with seeding a generator using another randomly generated integer,
    it is not recommended for practical applications that require massive amounts of different streams of random
    numbers to generate where the generators themselves are constantly reseeded. John Cook gives a good summary of
    the potential downfalls of seeding a generator with another random integer in a post here:
    https://www.johndcook.com/blog/2016/01/29/random-number-generator-seed-mistakes/.

    References
    ----------
    Combined Linear Congruential Generator. (2017, July 5). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Combined_Linear_Congruential_Generator&oldid=789099445

    Pierre L'Ecuyer (1988). Efficient and Portable Combined Random Number Generators.
        Communications of the ACM. 31: 742â749, 774. doi:10.1145/62959.62969

    Pierre L'Ecuyer, (1999) Good Parameters and Implementations for Combined Multiple Recursive Random Number Generators.
        Operations Research 47(1):159-164. doi.org/10.1287/opre.47.1.159

    """
    rn = []

    a1, a2 = 40014, 40692
    m1, m2 = 2147483563, 2147483399

    y1, y2 = np.random.randint(1, m1 - 1, 1), np.random.randint(1, m2 - 1, 1)

    for _ in np.arange(n):
        y1, y2 = a1 * y1 % m1, a2 * y2 % m2

        x = (y1 - y2) % (m1 - 1)

        if x > 0:
            r = x / m1
        elif x < 0:
            r = (x / m1) + 1
        else:  # x == 0
            r = (m1 - 1) / m1

        rn.append(r)

    if len(rn) == 1:
        rn = rn[0]

    return rn


def clcg_16bit(n=10):
    r"""
    Implementation of a combined linear congruential generator suited for 16-bit processors as proposed by
    L'Ecuyer.

    Parameters
    ----------
    n : int, default 10
        The number of random samples to generate

    Returns
    -------
    list or float
        If n is greater than 1, a list of the generated random values is returned. If n is equal to 1, the
        generated value is returned as float.

    Notes
    -----
    The 16-bit version of the combined linear congruential generator proceeds in the same way as the 32-bit
    version but uses three MCGs with the following parameters:

    .. math::

        a_1 = 157 \qquad m_1 = 32363 \qquad a_2 = 146 \qquad m_2 = 31727 \qquad a_3 = 142 \qquad m_3 = 31657

    See Also
    --------
    clcg_32bit() : Function
        32-bit implementation of a combined linear congruential generator as proposed by L'Ecuyer.

    References
    ----------
    Combined Linear Congruential Generator. (2017, July 5). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Combined_Linear_Congruential_Generator&oldid=789099445

    Pierre L'Ecuyer (1988). Efficient and Portable Combined Random Number Generators.
        Communications of the ACM. 31: 742â749, 774. doi:10.1145/62959.62969

    Pierre L'Ecuyer, (1999) Good Parameters and Implementations for Combined Multiple Recursive Random Number Generators.
        Operations Research 47(1):159-164. doi.org/10.1287/opre.47.1.159

    """
    rn = []

    a1, a2, a3 = 157, 146, 142
    m1, m2, m3 = 32363, 31727, 31657

    y1, y2, y3 = np.random.randint(1, m1 - 1, 1), np.random.randint(1, m2 - 1, 1), np.random.randint(1, m3 - 1, 1)

    for _ in np.arange(n):
        y1, y2, y3 = a1 * y1 % m1, \
                     a2 * y2 % m2, \
                     a3 * y3 % m3

        x = (y1 - y2 - y3) % (m1 - 1)

        if x > 0:
            r = x / m1
        elif x < 0:
            r = (x / m1) + 1
        else:  # x == 0
            r = (m1 - 1) / m1

        rn.append(r)

    if len(rn) == 1:
        rn = rn[0]

    return rn


def _generate_seed_number():

    return datetime.now().microsecond * 1000
