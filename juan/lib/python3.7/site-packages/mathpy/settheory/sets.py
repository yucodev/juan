# encoding=utf8


"""
Module containing Set class that extends the set class with additional methods.

"""


import pandas as pd


class Set(set):
    r"""
    The Set class provides additional methods not found in the :code:`set` class of base
    Python. Similar to the :code:`set` class, the :code:`Set` class can be initialized with
    an object or the methods can be called directly. The :code:`Set` class inherits the
    :code:`set` class methods.

    Attributes
    ----------
    x
        Initialized set object, optional.

    Methods
    -------
    cartesianproduct(a)
        Computes the Cartesian product of two sets.
    isequalset(a, *args)
        Tests if n number of sets are equivalent.
    ndifference(b, *args)
        Computes the relative complement of an arbitrary number of sets.
    nintersect(b, *args)
        Performs the set intersection operation on an arbitrary number of sets.
    nunion(b, *args)
        Performs the union set operation on an arbitrary number of sets.

    Examples
    --------
    >>> Set.cartesianproduct([1,2,3], [7,9,11])
    [{1, 7}, {1, 9}, {1, 11}, {2, 7}, {2, 9}, {2, 11}, {3, 7}, {3, 9}, {3, 11}]
    >>> Set([1,2,3]).cartesianproduct([7,9,11])
    [{1, 7}, {1, 9}, {1, 11}, {2, 7}, {2, 9}, {2, 11}, {3, 7}, {3, 9}, {3, 11}]
    >>> Set.ndifference([2,3,4,6], [3,4,5,7], [3,4,8,9])
    {2, 6}
    >>> Set([2,3,4,6]).ndifference([3,4,5,7], [3,4,8,9])
    {2, 6}

    """
    def __init__(self, x=None):
        if x is None:
            self.x = set()
        else:
            self.x = _convert_to_set(x)

        super(Set, self).__init__(self.x)

    def cartesianproduct(self, a):
        r"""
        Computes the Cartesian product of two sets.

        Parameters
        ----------
        a
            Second set to compute the Cartesian product.

        Returns
        -------
        list
            Cartesian product of two sets :math:`A` and :math:`B`. List is returned
            rather than a set to preserve order. Elements of the list are ordered pair
            sets.

        Notes
        -----
        The Cartesian product of two sets :math:`A` and :math:`B` is essentially a set
        of all ordered pairs between the two sets. An ordered pair, ex: :math:`\{2,3\}`,
        is denoted as :math:`\langle 2, 3 \rangle` and represents the relation of two sets.
        As such, :math:`\langle 2, 3 \rangle \neq \langle 3, 2 \rangle`.

        Examples
        --------
        >>> a, b = [1,2,3], [7,9,11]
        >>> Set.cartesianproduct(a, b)
        [{1, 7}, {1, 9}, {1, 11}, {2, 7}, {2, 9}, {2, 11}, {3, 7}, {3, 9}, {3, 11}]

        References
        ----------
        Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

        MacGillivray, G. Cartesian Products and Relations. Victoria, BC.
            Retrieved from http://www.math.uvic.ca/faculty/gmacgill/guide/RF.pdf

        Stacho, Juraj (n.d.). Cartesian Product [PowerPoint slides].
            Retrieved from http://www.cs.toronto.edu/~stacho/macm101.pdf

        """
        axb = []
        b = a

        if hasattr(self, 'x') is False:
            a = list(self)
        else:
            a = list(self.x)

        for j in a:
            for i in b:
                axb.append(set([i, j]))

        return axb

    def isequalset(self, b, *args):
        r"""
        Tests if given values coerced into set objects are equivalent.

        Parameters
        ----------
        b
            Second set to perform equality comparison. Can be a list, dictionary (keys will
            be used), pandas DataFrame (the first column of the DataFrame is used), pandas
            Series, or a numpy ndarray. Coerces the input into a :code:`set`.
        args
            Optional, additional sets.

        Returns
        -------
        bool
            True if the sets are equivalent, False otherwise

        Notes
        -----
        Set equality is defined by the Principle of Extensionality, one of the first axioms
        in the Zermelo-Fraenkel axiomatic system.

        The Principle of Extensionality states that if two sets have the same members, they
        are equal. Thus, the order of elements in two sets has no bearing on set equality.
        The Principle of Extensionality can be stated more formally as:

        .. math::

            \forall A \forall B (\forall x (x \in A \Leftrightarrow x \in B) \Rightarrow A = B)

        Examples
        --------
        >>> a, b, c = [2,3,1],[3,2,1],[1,2,3]
        >>> Set.isequalset(a, b, c)
        True
        >>> Set(a).isequalset(b, c)
        True

        References
        ----------
        Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

        """
        if hasattr(self, 'x') is False:
            u = list(self)
        else:
            u = list(self.x)

        if len(u) != len(b):
            return False

        for i in u:
            if i not in b:
                return False

        if args is not None:
            for i in args:
                s = _convert_to_set(i)
                for j in s:
                    if j not in b:
                        return False

        return True

    def ndifference(self, b, *args):
        r"""
        Computes the relative complement of an arbitrary number of sets. Extension
        of the :code:`difference()` method of the :code:`set` class.

        Parameters
        ----------
        b
            Second set to perform relative complement operation. Can be a list, dictionary (keys will
            be used), pandas DataFrame (the first column of the DataFrame is used), pandas
            Series, or a numpy ndarray. Coerces the input into a :code:`set`.
        args
            Optional, additional sets.

        Returns
        -------
        set
            Resulting set from relative complement operation(s).

        Notes
        -----
        The relative complement two sets :math:`A` and :math:`B` is defined as the members
        of :math:`A` not in :math:`B` and is denoted :math:`A - B`. The relative complement
        of two sets can also be written as :math:`A / B`. More formally, the relative
        complement of two sets is defined as:

        .. math::

            A - B = \{x \in A \space | \space x \notin B \}

        Examples
        --------
        >>> a, b, c = [2,3,4,6], [3,4,5,7], [3,4,8,9]
        >>> Set.ndifference(a, b, c)
        {2, 6}

        References
        ----------
        Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

        """
        d = []
        if hasattr(self, 'x') is False:
            u = list(self)
        else:
            u = list(self.x)

        for i in u:
            if i in u and i not in b:
                d.append(i)

        if args is not None:
            for i in args:
                s = _convert_to_set(i)
                for j in s:
                    if j in d:
                        d.remove(j)

        return set(d)

    def nintersect(self, b, *args):
        r"""
        Performs the set intersection operation on an arbitrary number of sets.
        Extension of the :code:`intersection()` method of the :code:`set` class.

        Parameters
        ----------
        b
            Second set to perform intersection operation. Can be a list, dictionary (keys will
            be used), pandas DataFrame (the first column of the DataFrame is used), pandas
            Series, or a numpy ndarray. Coerces the input into a :code:`set`.
        args
            Optional, additional sets.

        Returns
        -------
        set
            The set resulting from the union operations

        Notes
        -----
        For a nonempty set :math:`A`, a set :math:`B` exists such for any element :math:`x`:

        .. math::

            \forall a \space \forall b \exists B \space \forall x (x \in B \Leftrightarrow x \in a \space \wedge \space x \in b)

        This can be extended for an arbitrary number of set intersection operations. For example,
        the intersection of four sets :math:`\{a, b, c, d\}` can be written as the following:

        .. math::

            \forall a \space \forall b \space \forall c \space \forall d \exists B \space \forall x
            (x \in B \Leftrightarrow x \in a \space \wedge \space x \in b \wedge \space x \in c \wedge \space
            x \in d)

        Consider the four sets :math:`a = \{1,2,3,5\}, b = \{1,3,5\}, c = \{1,4,5,3\}, d = \{2,5,1,3\}`. The
        intersection of the sets can be denoted in a compact fashion:

        .. math::

            \bigcap \big\{a, b, c, d\big\} = \big\{\{1,2,3,5\}, \{1,3,5\}, \{1,4,5,3\}, \{2,5,1,3\}\big\}

        Which can also be written as:

        \{1,2,3,5\} \cap \{1,3,5\} \cap \{1,4,5,3\} \cap \{2,5,1,3\} = \{1,3,5\}

        Examples
        --------
        >>> a, b, c, d = [1,2,3,5], [1,3,5], [1,4,5,3], [2,5,1,3]
        >>> Set.nintersect(a, b, c, d)
        {1, 3, 5}

        References
        ----------
        Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

        """
        intersect = []

        if hasattr(self, 'x') is False:
            u = list(self)
        else:
            u = list(self.x)

        for i in b:
            if i in u:
                intersect.append(i)

        if args is not None:
            for i in args:
                s = _convert_to_set(i)
                for j in s:
                    if j in intersect:
                        intersect.append(j)

        return set(intersect)

    def nunion(self, b, *args):
        r"""
        Performs the union set operation on an arbitrary number of sets. Extension
        of the :code:`union()` method of the :code:`set` class.

        Parameters
        ----------
        b
            Second set to perform union operation. Can be a list, dictionary (keys will
            be used), pandas DataFrame (the first column of the DataFrame is used), pandas
            Series, or a numpy ndarray. Coerces the input into a :code:`set`.
        args
            Optional, additional sets.

        Returns
        -------
        set
            The set resulting from the union operations

        Notes
        -----
        The union axiom from the Zermelo-Fraenkel axiomatic system states for two sets
        :math:`A` and :math:`B`, there exists a set whose members consist entirely of
        those elements belonging to the two sets. The union axiom can be stated more
        formally:

        .. math::

            \forall a \space \forall b \space \exists B \space \forall x (x \in B \Leftrightarrow x \in a \space \vee \space x \in b)

        Thus for an arbitrary amount of sets, a restatement of the union axiom must be
        made. Define the union of an n number of sets as :math:`\bigcup A`, then the
        union axiom can be restated as:

        .. math::

            \large{x \in \bigcup A \Leftrightarrow (\exists b \in A) \space x \in b}

        For example, the union of four sets :math:`\{a,b,c,d\}` can be written as:

        .. math::

            \bigcup \{a, b, c, d \} = \big\{(\exists B \in A) \space x \in \{a, b, c, d\}\big\}

        Which is equivalent to:

        .. math::

            \bigcup \{a, b, c, d \} = a \cup b \cup c \cup d

        Examples
        --------
        >>> a, b, c, d = [1,2,3,5], [1,3,5], [1,4,5,3], [2,5,1,3]
        >>> Set.nunion(a, b, c, d)
        {1,2,3,4,5}
        >>> e, f, g = [2,4,6], [3,5,7], [2,3,8]
        >>> Set.nunion(e, f, g)
        {2, 3, 4, 5, 6, 7, 8, 9}

        References
        ----------
        Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

        """
        if hasattr(self, 'x') is False:
            u = list(self)
        else:
            u = list(self.x)

        for i in b:
            if i not in u:
                u.append(i)

        if args is not None:
            for i in args:
                s = _convert_to_set(i)
                for j in s:
                    if j not in u:
                        u.append(j)

        return set(u)


def iselement(x, a):
    r"""
    Tests if a given element belongs the set A. Essentially equivalent to :code:`x in A` and
    :code:`x not in A` for elements that are non-members of the set :math:`A`.

    Parameters
    ----------
    x
        Element to test if exists in set
    a
        The set to test

    Returns
    -------
    Boolean
        True if the element belongs to the set, False otherwise

    Notes
    -----
    Set membership is denoted as:

    .. math::

        x \in A

    Which is said as :math:`x` is an element of the set :math:`A`. If :math:`x` does not belong
    to the set, it is denoted as:

    .. math::

        x \notin A

    Examples
    --------
    >>> iselement(3, [3, 5, 7])
    True
    >>> iselement(4, [[2, 4, 6]])

    References
    -----
    Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

    """
    a = _convert_to_set(a)

    if x in a:
        return True
    else:
        return False


def issubset(a, b):
    r"""
    Tests if the set :math:`a` is a subset of the set :math:`b`. Recommended to use Python's
    built-in function :code:`issubset()` as part of the :code:`set` class. The function is
    given here to show the underlying logic for testing if a set is a subset of another set.

    Parameters
    ----------
    a
        Set to test if it is a subset of :math:`b`
    b
        Set to test to determine if :math:`a` is a subset of :math:`b`

    Returns
    -------
    Boolean
        Returns True if the set is a subset, False otherwise.

    Notes
    -----
    A set :math:`A` is a subset of a set :math:`B`, written :math:`A \subseteq B` if all the
    elements of :math:`A` are also elements of :math:`B`. Therefore, all sets are subsets of
    themselves and the empty set :math:`\varnothing` is a subset of every set.

    Examples
    --------
    >>> issubset([1,2,3], [1,2,3,4,5])
    True
    >>> issubset([3,5,6], [5,7,3])
    False

    References
    ----------
    Enderton, H. (1977). Elements of set theory (1st ed.). New York: Academic Press.

    """
    a, b = _convert_to_set(a), _convert_to_set(b)

    for i in a:
        if i not in b:
            return False

    return True


def _convert_to_set(x):
    if isinstance(x, (set, frozenset)):
        return x
    elif isinstance(x, pd.DataFrame):
        x = set(x.iloc[:, 0])
    else:
        x = set(x)

    return x
