import numpy as np
import matplotlib.pyplot as plt
import random
from trial import simulate_trial

class GeneticAlgorithm:
    def __init__(
        self,  
        n_genes,
        n_people,
        lawyer,
        jury_pool,
        testimonies,
        n_iterations = 8, # numero de iteraciones del algoritmo genetico
        n_estrategy = 5,
        n_jurors = 12, 
        population = None, # poblacion
        n_selected_individuals = 5, # numero de individuos a seleccionar
        fitness_func = None,
        case = None):   

        self.n_genes = n_genes 
        self.fitness_func = fitness_func
        self.n_iterations = n_iterations
        self.n_selected_individuals = n_selected_individuals 
        self.n_estrategy = n_estrategy
        self.population = population
        self.n_jurors = n_jurors 
        self.n_people = n_people
        self.lawyer = lawyer
        self.jury_pool = jury_pool
        self.testimonies = testimonies
        self.best_fitness_evolution = []
        self.most_popular_alleles = [[0, None]]*n_people
        self.best_solutions = []
        self.sequences_of_events = []
        self.case = case
        
        self.variance = 100

        # Asserts 
        # Check that fitness function is a function
        try:
            assert callable(fitness_func)
        except:
            print('The argument fitness_func is not a function')
    
    ## Method for evaluation
    def get_fitness_scores(self):
        scores = []
        for ind in self.population:
            score, _, text = self.fitness_func(ind, self.n_jurors, self.testimonies, self.jury_pool, self.lawyer, self.case)
            scores.append(score)
            self.sequences_of_events.append(text)

        # scores = [self.fitness_func(ind, self.n_jurors, self.testimonies, self.jury_pool, self.lawyer)[0] for ind in self.population]
        return np.array(scores)
    
    def reset_popular_alleles(self):
        self.most_popular_alleles = [[0,number] for number in range(1,self.n_people+1)]
    
    def get_popular_alleles(self, population):
        for ind in population:
            for elem in ind[:self.n_jurors]:
                self.most_popular_alleles[elem-1][0] += 1
        self.most_popular_alleles.sort()

    def get_allele(self, individual, elem):
        number_used = [False]*(self.n_people+1)
        for ind in individual:
            number_used[ind] = True
        for allele in self.most_popular_alleles:
            if(not number_used[allele[1]]):
                return allele[1]
            
        return elem
    
    # Method to save the best score in each iteration
    def __append_best_score(self, scores):
        best_score = np.max(scores)
        self.best_fitness_evolution.append(best_score)

        scores = [(score, pos) for pos, score in enumerate(scores)]
        scores.sort()
        best_score_ind = scores[-1][1]
        best_solution = self.population[best_score_ind]

        text = self.sequences_of_events[best_score_ind]

        self.best_solutions.append((best_solution, best_score, text))
        return 'Ok'
    
    ## Selection of individuals by ranking
    def __ranking_selection(self, scores, k):
        if k is None:
            raise ValueError('K must not be none if type ranking is selected.')
        
        scores = [(score, pos) for pos, score in enumerate(scores)]
        scores.sort()
        scores.reverse()
        ind = np.array([pos for score, pos in scores])[:k]

        return ind
    
    ## Methods to create new descendants
    # Function to create new descendants through the combination of their parents (one point)
    def __crossover(self, parent1, parent2):
        
        parents = [parent1, parent2]

        # Chromosomes arranged at one point for jurors
        indexJ = np.random.choice(range(self.n_jurors))
        childrenJ = [None]*2
        for i in [0,1]: 
            numbers_used = [False]*(self.n_people+1)
            tupl = list(parents[i][:indexJ])
            size_tupl = len(tupl)
            for elem in tupl:
                numbers_used[elem] = True
            tupl = tupl + list(parents[i][indexJ:self.n_jurors]) 

            pointer = indexJ
            ptr_tuple = indexJ
            iterations = 1
            while(size_tupl < self.n_jurors and iterations <= self.n_jurors):
                x = parents[i^1][pointer]
                if(not numbers_used[x]):
                    tupl[ptr_tuple] = x
                    numbers_used[x] = True
                    size_tupl = size_tupl + 1
                    ptr_tuple = ptr_tuple + 1
                if(pointer == self.n_jurors-1):
                    pointer = 0
                else:
                    pointer = pointer + 1
                iterations = iterations + 1
            
            childrenJ[i] = tuple(tupl)

        # One point for strategy
        indexS = np.random.choice(range(self.n_jurors, len(parent1)))
        childrenS = [parent2[self.n_jurors:indexS] + parent1[indexS:], parent1[self.n_jurors:indexS] + parent2[indexS:]]

        return [childrenJ[1] + childrenS[0], childrenJ[0] + childrenS[1]]
    
    # Function to create new descendants through the mutation of a parent
    def __mutation(self, individual):

        # Get index of individual to modify
        index = np.random.choice(len(individual))

        # Convert individual to list so that can be modified
        individual_mod = list(individual)

        # Change the value
        if(index < self.n_jurors):
            individual_mod[index] = self.get_allele(individual, individual_mod[index])
        else:
            individual_mod[index] = individual_mod[(len(individual) - 1) - index + self.n_jurors]
        
        # Convert individual to tuple
        individual = tuple(individual_mod)

        return individual

    def optimize(self):
        
        for _ in range(self.n_iterations):
        # while self.variance > 0.01 and self.n_iterations > 0:
            ## Calculate fitness score
            self.sequences_of_events = []
            scores = self.get_fitness_scores()
            # self.variance = np.var(np.array(scores))

            # Append best score
            _ = self.__append_best_score(scores)

            ## Make Selection
            selected_genes = self.__ranking_selection(scores, self.n_selected_individuals)

            ## Crossover
            # Get pairs of parents
            parents_pairs = np.random.choice(
                selected_genes,
                (int(self.n_genes/2),2)
            )
            
            # For each pair, make crossover
            new_population = [self.__crossover(self.population[parents[0]], self.population[parents[1]])
                                for parents in parents_pairs]
            # Unnest population
            new_population = [child for children in new_population for child in children]

            # Get popular jurors
            self.reset_popular_alleles()
            self.get_popular_alleles(new_population)

            ## Mutation
            new_population = [self.__mutation(ind)
                for ind in new_population]
            
            # Set new population as population
            self.population = new_population
          # self.n_iterations -= 1
        
        # When n_iterations are finished, fitness score
        self.sequences_of_events = []
        scores = self.get_fitness_scores()

        # Append best score
        _ = self.__append_best_score(scores)

        return self.best_solutions

    def view_fitness_evolution(self):
        plt.plot(
            range(len(self.best_fitness_evolution)),
            self.best_fitness_evolution
        )
        plt.show()

def genetic_algorithm(lawyer, n_jurors, jury_pool, testimonies, case):
    # Poblacion random para la primera generacion del algoritmo genetico
    n_people = len(jury_pool)
    n_strategies = len(lawyer.strategies[0])
    n_testimonies = len(testimonies)
    poblacion = [
        tuple(random.sample(range(1, n_people+1), n_jurors)) + tuple(np.random.randint(1, n_strategies+1) for _ in range(n_testimonies))
        for _ in range(10)
    ]

    ga = GeneticAlgorithm(
        n_genes = 10,
        n_estrategy=n_strategies,
        n_jurors=n_jurors,
        population = poblacion,
        n_people = n_people,
        lawyer = lawyer,
        jury_pool = jury_pool,
        testimonies = testimonies,
        fitness_func= simulate_trial,
        case=case
    )

    # ga.view_fitness_evolution()
    return ga.optimize()  