import itertools

import numpy as np
from scipy.linalg import toeplitz

from mathpy._lib import _create_array


def simulate_corr_matrix(k=None, nk=None, rho=None, M=None, power=None, method=None):

    x = _CorMatrixSim(k, nk, rho, M, power)
    if method is None:
        c = getattr(x, x.method, None)
    else:
        if hasattr(x, method):
            c = getattr(x, method, x.method)
        else:
            return 'no attribute with name ' + str(method)

    return c()


def add_noise(cor, epsilon=None, M=None):
    x = _create_array(cor)[0]
    n = x.shape[1]

    if epsilon is None:
        epsilon = 0.05
    if M is None:
        M = 2

    np.fill_diagonal(cor, 1 - epsilon)

    cor = _CorMatrixSim._generate_noise(cor, n, M, epsilon)

    return cor


class _CorMatrixSim(object):

    def __init__(self, k=None, nk=None, rho=None, M=None, power=None):

        if k is None:
            self.k = np.random.randint(3, 10)
        else:
            self.k = k
        if M is None:
            self.M = np.random.randint(1, 4)
        else:
            self.M = M
        if nk is None:
            self.nk = np.random.randint(2, 5, self.k)
        else:
            self.nk = nk
        if rho is None:
            self.rho = np.random.rand(self.k)
        else:
            self.rho = rho
        if power is None:
            self.power = 1
        else:
            self.power = power

        self.nkdim = int(np.sum(self.nk))
        self.method = 'constant'

    def constant(self):
        delta = np.min(self.rho) - 0.01
        cormat = np.full((self.nkdim, self.nkdim), delta)

        epsilon = 0.99 - np.max(self.rho)
        for i in np.arange(self.k):
            cor = np.full((self.nk[i], self.nk[i]), self.rho[i])

            if i == 0:
                cormat[0:self.nk[0], 0:self.nk[0]] = cor
            if i != 0:
                cormat[np.sum(self.nk[0:i]):np.sum(self.nk[0:i + 1]),
                np.sum(self.nk[0:i]):np.sum(self.nk[0:i + 1])] = cor

        np.fill_diagonal(cormat, 1 - epsilon)

        cormat = self._generate_noise(cormat, self.nkdim, self.M, epsilon)

        return cormat

    def toepz(self):
        cormat = np.zeros((self.nkdim, self.nkdim))

        epsilon = (1 - np.max(self.rho)) / (1 + np.max(self.rho)) - .01

        for i in np.arange(self.k):
            t = np.insert(np.power(self.rho[i], np.arange(1, self.nk[i])), 0, 1)
            cor = toeplitz(t)
            if i == 0:
                cormat[0:self.nk[0], 0:self.nk[0]] = cor
            if i != 0:
                cormat[np.sum(self.nk[0:i]):np.sum(self.nk[0:i + 1]),
                np.sum(self.nk[0:i]):np.sum(self.nk[0:i + 1])] = cor

        np.fill_diagonal(cormat, 1 - epsilon)

        cormat = self._generate_noise(cormat, self.nkdim, self.M, epsilon)

        return cormat

    def hub(self):
        cormat = np.zeros((self.nkdim, self.nkdim))

        for i in np.arange(self.k):
            cor = toeplitz(self._fill_hub_matrix(self.rho[i,0],self.rho[i,1], self.power, self.nk[i]))
            if i == 0:
                cormat[0:self.nk[0], 0:self.nk[0]] = cor
            if i != 0:
                cormat[np.sum(self.nk[0:i]):np.sum(self.nk[0:i + 1]),
                np.sum(self.nk[0:i]):np.sum(self.nk[0:i + 1])] = cor
            tau = (np.max(self.rho[i]) - np.min(self.rho[i])) / (self.nk[i] - 2)

        epsilon = 0.08 #(1 - np.min(rho) - 0.75 * np.min(tau)) - 0.01

        np.fill_diagonal(cormat, 1 - epsilon)

        cormat = self._generate_noise(cormat, self.nkdim, self.M, epsilon)

        return cormat

    @staticmethod
    def _generate_noise(cormat, N, M, epsilon):
        ev = []
        for _ in itertools.repeat(None, N):
            ei = np.random.uniform(low=-1, high=1, size=M)
            ev.append(np.sqrt(epsilon) * ei / np.sqrt(np.sum(np.power(ei, 2))))

        ev = np.array(ev).T
        E = np.dot(ev.T, ev)
        cormat = cormat + E

        return cormat

    @staticmethod
    def _fill_hub_matrix(rmax, rmin, power, p):
        rho = np.empty(p)
        rho[0] = 1
        for i in np.arange(1, p):
            rho[i] = rmax - np.power((i - 1) / (p - 1), power * (rmax - rmin))

        return rho