"""
Create lattices, simulate models on them and animate the result
"""

import numpy as np
import numpy.random as npr

import matplotlib.pyplot as plt
import matplotlib.animation as anime

from automata import GameOfLife, SnowDrift


def add_glider(pos, mat):
    """ Add glider to state at given position (row, col)
    """
    row, col = pos

    mat[row, col-1] = 1
    mat[row+1, col] = 1
    mat[row+1, col+1] = 1
    mat[row, col+1] = 1
    mat[row-1, col+1] = 1

    return mat

def animate(evolution, out_file='out.gif'):
    """ Create animation from list of images
    """
    fig = plt.figure()
    plt.axis('off')

    img = plt.imshow(evolution[0], cmap='Greys', interpolation='nearest')
    def update_func(i):
        """ Generate frame `i` of the animation
        """
        img.set_array(evolution[i])
        return img,

    anim = anime.FuncAnimation(
        fig, update_func,
        range(len(evolution)),
        interval=100
        #blit=True
    )
    #plt.show()

    anim.save(out_file, writer='imagemagick')

def setup_lattice():
    """ Populate lattice with its initial configuration
    """
    #mat = np.zeros((15, 15))
    #mat = add_glider((7, 2), mat)

    mat = npr.random_integers(0, 1, size=(15, 15))

    return mat

def simulate(Model):
    """ Simulate given model
    """
    lattice = setup_lattice()

    evolution = []
    for grid in Model(lattice).iterate(100):
        evolution.append(grid)

    animate(evolution)

def main():
    """ Have fun :-)
    """
    #simulate(GameOfLife)
    simulate(SnowDrift)

if __name__ == '__main__':
    main()
