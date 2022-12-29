
import random
#from random import choice

def tournamentSelect(candidateInput, tournamentSize, returnAmount):
    # put list of tuples
    # select n from list
    # return best 2
    candidates = candidateInput.copy()
    tournament = []
    for _ in range(tournamentSize):
        item = random.choice(candidates)
        candidates.remove(item)
        tournament.append(item)
    return (sorted(tournament))[:returnAmount]



'''
TODO SEPT 19 2022:
As per 1801.02335,

Clean Repo of everything not needed / clean up structures, names, error checking, random generation constants, limits and stuff

Algorithm Updates:
0. Get fitness-ordered set of candidates

1. Crossover Parent Selection:
    - Tournament Selection:
        - Choose n candidates at random from whole list (higher n is less variation?)
        - select best 2, or have some weighted probability based on fitness for best 2 (Rank Selection?)
    - Rank Selection:
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