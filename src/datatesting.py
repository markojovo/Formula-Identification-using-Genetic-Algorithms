from typing import Dict
from function_tree import evaluate
import math
from function_tree import FunctionTree, get_random_func, evaluate, CHILDREN_KEY, NAME_KEY, to_lisp, MAX_DEPTH

def extract_data(filename):
    count = 0
    weekly_infections = [0] * 53                # initialize empty array for infections per week
    with open(filename) as f:                   # open the file with the dataset
        for line in f:                          # for each datapoint in the dataset
            currentline = line.split(",")       # separate week of infection (and other variables) from its continuous string
            if count > 0:                       # Skip first line of the dataset, because it's strings only
                week_infected = int(currentline[2])  # extract week infected
                if week_infected <= 52:         # omit data beyond the first year
                    weekly_infections[week_infected] += 1  # increase # of infections that week by 1.
            count += 1
    weekly_infections.pop(0)  # remove first index being 0
    print(weekly_infections)  # printing just to get an idea of what it looks like
    return weekly_infections

def score_a_function(weekly_infections, root: FunctionTree, variables):
    i = 0
    total = 0
    while i < 52:
        variables.update({'infection': weekly_infections[i]})
        total+= ( weekly_infections[i] - (evaluate(root, variables))**2 ) / 52
        i += 1
    return total

def find_a_winner(list_of_roots,weekly_infections,variables):
    i = 0
    winner = list_of_roots[0]
    min_score = math.inf
    while i < len(list_of_roots):
        new_score = score_a_function(weekly_infections,list_of_roots[i],variables)
        if new_score < min_score:
            winner = list_of_roots[i]
            min_score = new_score
        i += 1
    return winner


