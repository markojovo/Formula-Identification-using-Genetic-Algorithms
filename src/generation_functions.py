from sys import float_info
from random import random, randint, gauss
from function_tree import FunctionTree, get_random_func, evaluate, CHILDREN_KEY, NAME_KEY, to_lisp, MAX_DEPTH
from genetic_operators import crossover, random_mutation
#from main import TARGET_VAL


class generation:
    unique_item_ID = 0
    funcs_list = []
    size = 0
    variables = {}
    TARGET_VALS = []
    #(score, insertion number, tree)


    def __init__(self, size, variables, TARGET_VALS):
        self.size = size
        self.variables = variables
        self.TARGET_VALS = TARGET_VALS
        for i in range(size):
            ############### REWRITE ######################
            self.add_to_generation(self.funcs_list, get_random_func(self.variables,round(abs(gauss(MAX_DEPTH-1,2))+1)))
            ##############################################

    def add_to_generation(self, generation_list, func_tree):
        self.unique_item_ID = self.unique_item_ID + 1
        generation_list.append( ( self.get_fitness(func_tree, self.variables), self.unique_item_ID, func_tree ) )
        #Stored in tuple form of (fitness, insertion order, function tree)

    def get_best_candidate(self):
            return sorted(self.funcs_list)[0][2]

    def evolve(self, elitism_amount, crossover_probability, replication_probability): #rest are mutated  
        prev_func_list = sorted(self.funcs_list.copy()) #Sorted by score
        new_func_list = []


        ############### REWRITE ######################
        # Elitism
        for i in range(elitism_amount):
            elite_specimen = prev_func_list.pop(0)[2]
            self.add_to_generation(new_func_list, elite_specimen)
            #self.add_to_generation(new_func_list, elite_specimen)
            
        # Genetic Operators
        while(len(prev_func_list) > 0):
            ratio = random() # Random float from 0 to 1
            tree_A = prev_func_list.pop(0)[2]

            if (len(to_lisp(tree_A)) > 50):
                self.add_to_generation(new_func_list, get_random_func(self.variables,round(abs(gauss(MAX_DEPTH-1,2))+1)))

            elif (ratio < crossover_probability / 2 and len(prev_func_list) > 1):
                tree_B = prev_func_list.pop(randint(0, len(prev_func_list)-1 ))[2] #select another random item from list
                [new_tree_A, new_tree_B] = crossover(tree_A, tree_B)

                self.add_to_generation(new_func_list, new_tree_A)
                self.add_to_generation(new_func_list, new_tree_B)


            elif (ratio < (replication_probability + crossover_probability/2)):
                self.add_to_generation(new_func_list, tree_A)

            else:
                self.add_to_generation(new_func_list, random_mutation(tree_A, self.variables))

        ##############################################

        self.funcs_list = new_func_list.copy()



    def get_fitness(self, temp_func, variables):
        try:
            sum_fitness = 0
            for i in range(len(self.TARGET_VALS)):
                variables['x'] = i
                sum_fitness = sum_fitness + (self.TARGET_VALS[i] - evaluate(temp_func, variables))**2 #+ 0.05*len(to_lisp(temp_func))
            sum_fitness = sum_fitness + len(to_lisp(temp_func))
            return sum_fitness
        except OverflowError:
            return float_info.max

'''
TODO SEPT 19 2022:
As per 1801.02335,

Clean Repo of everything not needed / clean up structures and names

Algorithm Updates:
0. Get fitness-ordered set of candidates

1. Crossover Parent Selection:
    - Rank selection:
        - Choose n candidates at random from whole list (higher n is less variation?)
        - select best 2, or have some weighted probability based on fitness for best 2 (Rank Selection?)
    - Rank selection:
        - Make "roulette wheel" with pi slice areas proportional to rank
        - ie randomly generate int between 1 and sum_max
            - where area_0 + area_1 + area_2 + ... + area_N = sum_max
            - and area_0 = 1, area_2 = 1/2, area_3 = 1/3... (or something similar)
    - Good Resource to Look At:
                http://www.ijmlc.org/papers/146-C00572-005.pdf

2. Crossovers (high [ie 85%] chance for crossovers):
    - use SBC (select best crossover)
        - Perform many crossovers of different variations between the two parents 
            (Need to somehow get set of all possible crossovers and choose from that, removing for each one completed)
        - Select the best 2 children from this set to be sent into the next step for mutation

3. Mutations (low [ie 5%] chance for mutations):
    - chance to apply to all candidates at this stage, whether crossovered or passed-through

'''