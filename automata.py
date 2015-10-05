"""
Implementation of several spatial models running on a lattice
"""

import numpy as np

from progressbar import ProgressBar


class CellularAutomaton(object):
    """ General CA class
    """

    def __init__(self, lattice):
        self.lattice = lattice

    def setup(self):
        """ This function is called before any iteration step takes place
        """
        pass

    def apply_rule(self, mat):
        """ Return the new lattice
        """
        raise NotImplementedError

    def iterate(self, steps):
        """ Yield each step up to `steps` of the current CA
        """
        self.setup()

        yield self.lattice
        pbar = ProgressBar()
        for _ in pbar(range(steps)):
            self.lattice = self.apply_rule(self.lattice)
            yield self.lattice

    def get_neighbours(self, pos, mat=None):
        """ Get elements in Moore neighborhood of given position.
            If no particular matrix is specified,
            the current lattice will be used.
        """
        if mat is None:
            mat = self.lattice

        r, c = pos
        nr = r+1 if r+1 < mat.shape[0] else 0
        nc = c+1 if c+1 < mat.shape[1] else 0

        positions = [
            (r-1, c-1), (r-1, c), (r-1, nc),
            (r, c-1), (r, nc),
            (nr, c-1), (nr, c), (nr, nc)
        ]

        return [(mat[row, col], (row, col)) for row, col in positions]

class GameOfLife(CellularAutomaton):
    """ Simulate Conway's Game of Life
    """

    def apply_rule(self, mat):
        """ Possibly the worst implementation of Game of life ever
        """
        next_mat = np.zeros(mat.shape)
        for row in range(mat.shape[0]):
            for col in range(mat.shape[1]):
                num = sum([e for e, p in self.get_neighbours((row, col))])
                if mat[row, col] == 1:
                    if num >= 2 and num <= 3:
                        next_mat[row, col] = 1
                else:
                    if num == 3:
                        next_mat[row, col] = 1

        return next_mat

class SnowDrift(CellularAutomaton):
    """ Simulate game according to some payoff matrix
    """

    def setup(self):
        """ Generate payoff matrix. It's of the form
            [
                [<C-C>, <C-D>],
                [<D-C>, <D-D>]
            ]
            C -> cooperate
            D -> defect
        """
        self.benefit = 0.6
        self.cost = 0.2

        self.payoff_mat = np.array([
            [self.benefit - self.cost / 2, self.benefit - self.cost],
            [self.benefit, 0]
        ])

    def get_payoff(self, own_strat, other_strat):
        """ Get corresponding payoff.
            Assume existance of only two strategies:
                0 -> cooperate
                1 -> defect
        """
        return self.payoff_mat[own_strat, other_strat]

    def apply_rule(self, mat):
        """ Some stuff
        """
        next_mat = np.zeros(mat.shape)
        fitness_mat = np.zeros(self.lattice.shape)

        # compute fitness matrix
        for row in range(mat.shape[0]):
            for col in range(mat.shape[1]):
                cur = mat[row, col]

                ns = self.get_neighbours((row, col))
                fitness = 0
                for n, p in ns:
                    fitness += self.get_payoff(cur, n)
                fitness /= len(ns)
                fitness_mat[row, col] += fitness

        # let the games begin
        for row in range(mat.shape[0]):
            for col in range(mat.shape[1]):
                curf = fitness_mat[row, col]
                nsf = self.get_neighbours((row, col), mat=fitness_mat)

                for nf, p in nsf:
                    if nf > curf:
                        next_mat[row, col] = mat[p[0], p[1]]
        return next_mat
