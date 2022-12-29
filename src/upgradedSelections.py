'''
TODO SEPT 19 2022:
As per 1801.02335,

Clean Repo of everything not needed / clean up structures, names, error checking, random generation constants, limits and stuff

Algorithm Updates:
0. Get fitness-ordered set of candidates

1. Crossover Parent Selection:
    - Tournament Selection:   ~~~ DONE ~~~
        - Choose n candidates at random from whole list (higher n is less variation?)   ~~~ DONE ~~~
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
    - chance to apply to all candidates at this stage, whether crossovered or passed-through   ~~~ DONE ~~~



Dec 29, 2022 Updates:
Done:
- Implemented tournament selection
- Performed mutations at a set rate irrespective of if cross-overed or passed-through (except elitism)
- Messed with parameters
Results
- Seemed to have better results? hard to tell
- Still has problem of non-convergence, seems to consistently fall into local minima of "Pick y = avg(data)"
- Need to somehow improve selection pressure to not be as penalized for using unique solutions that may end up having larger cost in interstitial evolutionary stages
- Basically my suspicion is this:
    - Most functions that aren't 
TODO:
- Continue with above changes, see how it goes
- will need to see experiments once fully implemented, but focus is on improving ability for algorithm to explore, while better able to follow if it figures out a good base (I think SBC could help w this, maybe some sort of look-ahead for the next-stage crossovers when evaluating the fitness of a function?)
'''


import random
#from random import choice

def tournamentSelect(candidates, tournamentSize, returnAmount):
    # put list of tuples
    # select n from list
    # return best 2
    tournament = random.sample(candidates, tournamentSize)
    return (sorted(tournament))[:returnAmount]



