from audioop import cross
from hashlib import new
from msilib import add_tables
from operator import ge
from sqlite3 import adapt
from sys import float_info
from tempfile import tempdir
from typing import Dict
from random import random, randint, choice, gauss
from numpy import var
from sympy import re
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
            self.add_to_generation(self.funcs_list, get_random_func(self.variables,round(abs(gauss(MAX_DEPTH-1,2))+1)))

    def add_to_generation(self, generation_list, func_tree):
        '''i = 0
        while((self.temp_fitness(func_tree, self.variables), i, func_tree) in generation_list):
            i = i + 1
        generation_list.append(tuple([self.temp_fitness(func_tree, self.variables), i, func_tree])) # storing functions in tuples to be able to sort by score'''


        self.unique_item_ID = self.unique_item_ID + 1
        generation_list.append( ( self.temp_fitness(func_tree, self.variables), self.unique_item_ID, func_tree ) )
        #Stored in tuple form of (fitness, insertion order, function tree)

    def get_best_candidate(self):
            return sorted(self.funcs_list)[0][2]
        


    def get_longest_candidate(self):
        max_len = 0
        candidate = None
        for i in self.funcs_list:
            if (len(to_lisp(i[2])) > max_len):
                candidate = i[2]
                max_len = len(to_lisp(candidate))
        return max_len

    def evolve(self, elitism_amount, crossover_probability, replication_probability): #rest are mutated  
        prev_func_list = sorted(self.funcs_list.copy()) #Sorted by score
        new_func_list = []

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


        self.funcs_list = new_func_list.copy()



    def temp_fitness(self, temp_func, variables):
        try:
            sum_fitness = 0
            for i in range(len(self.TARGET_VALS)):
                variables['x'] = i
                sum_fitness = sum_fitness + (self.TARGET_VALS[i] - evaluate(temp_func, variables))**2 #+ 0.05*len(to_lisp(temp_func))
            sum_fitness = sum_fitness + len(to_lisp(temp_func))
            return sum_fitness
        except OverflowError:
            return float_info.max

