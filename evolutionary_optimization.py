"""
Evolutionary optimization of something
"""

import random

import numpy as np
import numpy.random as npr

from automata import SnowDrift


class EvolutionaryOptimizer(object):
    """ Optimize!
    """
    def __init__(self):
        """ Set some parameters
        """
        self.mutation_probability = 0.02

    def init(self, size):
        """ Generate initial population
        """
        raise NotImplementedError

    def get_fitness(self, obj):
        """ Compute fitness of individual of population
        """
        raise NotImplementedError

    def mutate(self, obj):
        """ Mutate single individual
        """
        raise NotImplementedError

    def crossover(self, mom, dad):
        """ Generate offspring from parents
        """
        raise NotImplementedError

    def run(self, size, max_iter=100):
        """ Let life begin
        """
        population = self.init(size)

        for _ in range(max_iter):
            #print(population)
            pop_fitness = [self.get_fitness(o) for o in population]
            #print(pop_fitness)

            # crossover best individuals and replace worst with child
            best_indiv = np.argpartition(pop_fitness, -2)[-2:]
            mom, dad = population[best_indiv]
            child = self.crossover(mom, dad)
            #print(mom, dad, '->', child)

            worst_indiv = np.argmin(pop_fitness)
            population[worst_indiv] = child

            # apply mutations
            mut = lambda o: \
                self.mutate(o) if random.random() < self.mutation_probability \
                else o
            population = np.array([mut(o) for o in population])

            print('Mean individual:', np.mean(population, axis=0))
            #print()
            yield np.mean(population, axis=0)

class SnowdriftOptimizer(EvolutionaryOptimizer):
    """ Optimize snowdrift game by assuming each individual to be the pair of
        benefit and cost floats
    """
    def init(self, size):
        pop = []
        for _ in range(size):
            pop.append((random.uniform(0, 1), random.uniform(0, 1)))
        return np.array(pop)

    def crossover(self, mom, dad):
        return np.mean([mom, dad], axis=0)

    def mutate(self, obj):
        sigma = 0.05
        return (obj[0] * random.gauss(1, sigma), obj[1] * random.gauss(1, sigma))

    def get_fitness(self, obj):
        # setup system
        lattice = npr.random_integers(0, 1, size=(15, 15))
        model = SnowDrift(lattice)

        # generate dynamics
        iter_num = 100

        benefit, cost = obj
        res = list(model.iterate(iter_num, benefit=benefit, cost=cost))

        # cut off transient
        ss = res[-int(iter_num/10):]

        # compute fitness
        fit = -np.sum(ss)
        return fit

def main():
    """ Setup environment
    """
    opti = SnowdriftOptimizer()
    opti.run(4)

if __name__ == '__main__':
    main()
