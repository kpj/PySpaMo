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

    def apply_rule(self, mat):
        """ Return the new lattice
        """
        raise NotImplementedError

    def iterate(self, steps):
        """ Yield each step up to `steps` of the current CA
        """
        yield self.lattice
        pbar = ProgressBar()
        for _ in pbar(range(steps)):
            self.lattice = self.apply_rule(self.lattice)
            yield self.lattice

class GameOfLife(CellularAutomaton):
    """ Simulate Conway's Game of Life
    """

    def apply_rule(self, mat):
        """ Possibly the worst implementation of Game of life ever
        """
        def get_neighbor_num(pos):
            """ Get number of neighbors in Moore neighborhood of given position
            """
            r, c = pos
            nr = r+1 if r+1 < mat.shape[0] else 0
            nc = c+1 if c+1 < mat.shape[1] else 0

            return sum([
                mat[r-1, c-1], mat[r-1, c], mat[r-1, nc],
                mat[r, c-1],                mat[r, nc],
                mat[nr, c-1], mat[nr, c], mat[nr, nc]
            ])

        next_mat = np.zeros(mat.shape)
        for row in range(mat.shape[0]):
            for col in range(mat.shape[1]):
                num = get_neighbor_num((row, col))
                if mat[row, col] == 1:
                    if num >= 2 and num <= 3:
                        next_mat[row, col] = 1
                else:
                    if num == 3:
                        next_mat[row, col] = 1

        return next_mat
