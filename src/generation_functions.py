from sys import float_info
from random import random, randint, gauss, choice
from function_tree import FunctionTree, get_random_func, evaluate, CHILDREN_KEY, NAME_KEY, to_lisp, MAX_DEPTH
from genetic_operators import crossover, random_mutation
from upgradedSelections import tournamentSelect
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

    def evolve(self, elitism_amount, crossover_probability, mutation_probability): #rest are mutated  
        prev_func_list = sorted(self.funcs_list.copy()) #Sorted by score
        new_func_list = []


        #####################################
        # Elitism
        for i in range(elitism_amount):
            elite_specimen = prev_func_list.pop(0)[2]
            self.add_to_generation(new_func_list, elite_specimen)
            #self.add_to_generation(new_func_list, elite_specimen)
            

        # Genetic Operators
        while(len(prev_func_list) > 0):
            crossRandom = random() # Random float from 0 to 1
            mutRandom = random()

            if (crossRandom < crossover_probability/2 and len(prev_func_list) > 25):
                performingCrossover = True
                [tree_A, tree_B] = tournamentSelect(prev_func_list, 25, 2)
                prev_func_list.remove(tree_A)
                prev_func_list.remove(tree_B)
                new_tree_A = tree_A[2]
                new_tree_B = tree_B[2]
                [new_tree_A, new_tree_B] = self.select_best_crossover(new_tree_A, new_tree_B, 10)

                if (len(to_lisp(new_tree_A)) > 50):
                    new_tree_A = get_random_func(self.variables,round(abs(gauss(MAX_DEPTH-1,2))+1))
                if (len(to_lisp(new_tree_B)) > 50):
                    new_tree_A = get_random_func(self.variables,round(abs(gauss(MAX_DEPTH-1,2))+1))
            else:
                performingCrossover = False
                tree_A = choice(prev_func_list)
                prev_func_list.remove(tree_A)
                new_tree_A = tree_A[2]
                if (len(to_lisp(new_tree_A)) > 50):
                    new_tree_A = get_random_func(self.variables,round(abs(gauss(MAX_DEPTH-1,2))+1))



            if (mutRandom < mutation_probability):
                self.add_to_generation(new_func_list, random_mutation(new_tree_A, self.variables))
                if (performingCrossover):
                    self.add_to_generation(new_func_list, random_mutation(new_tree_B, self.variables))        
            else:
                self.add_to_generation(new_func_list, new_tree_A)
                if (performingCrossover):
                    self.add_to_generation(new_func_list, new_tree_B)




        ##############################################

        self.funcs_list = new_func_list.copy()



    def get_fitness(self, temp_func, variables):
        try:
            sum_fitness = 0
            for i in range(len(self.TARGET_VALS)):
                variables['x'] = i
                sum_fitness = sum_fitness + (self.TARGET_VALS[i] - evaluate(temp_func, variables))**2 + 0.05*len(to_lisp(temp_func))
            sum_fitness = sum_fitness + len(to_lisp(temp_func))
            return sum_fitness
        except OverflowError:
            return float_info.max


    def select_best_crossover(self, rootA, rootB, numCrossovers):
        currBestScore = float_info.max
        bestA = rootA
        bestB = rootB
        for _ in range(numCrossovers):
            [a,b] = crossover(rootA.copy(), rootB.copy()) # Need to double check if crossover affects original roots
            if (self.get_fitness(a, self.variables) < currBestScore):
                currBestScore = self.get_fitness(a, self.variables)
                bestA = a
                bestB = b

            elif (self.get_fitness(b, self.variables) < currBestScore ):
                currBestScore = self.get_fitness(b, self.variables)
                bestA = a
                bestB = b

        return [bestA, bestB]



