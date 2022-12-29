
import matplotlib.pyplot as plt
from datatesting import extract_data
from function_tree import evaluate, to_lisp, get_random_func
from genetic_operators import cut_and_grow, shrink, hoist, crossover
from generation_functions import generation
from math import pi, log, sin, exp
from sys import float_info

variables = {
    'x':1
}

#NUM_DATA_POINTS = 150

'''def mathFunc(x):
    if x < NUM_DATA_POINTS/2:
        return 10*sin(3*x) + 2*x
    else:
        return 10*sin(3*x)
'''

input_array = extract_data('COVID19-eng.csv')
#normalization_coeff = 10/(max(input_array))
#for i in range(len(input_array)):
#    input_array[i] = input_array[i]*normalization_coeff

#print(input_array)

#for k in range(NUM_DATA_POINTS):
#    input_array.append(mathFunc(k))






'''
for i in range(1000):
    print("Generation Number: " +str(i+2))
    gen.evolve(10,0.4,0.3)
'''


genNum = 1
MAX_GEN_NUM = 150000
num_of_gens = 1

best_of_runs = []

exit_flag = False

'''for _ in range(num_of_gens):
    if exit_flag:
        continue'''
gen = generation(2500, variables, input_array)
#try:
if (True):
    while(True):


        print("Generation Number: " +str(genNum))
        best_candidate = gen.get_best_candidate()
        print("Best Candidate: "+to_lisp(gen.get_best_candidate()))
        #print("Longest candidate length: "+ str(gen.get_longest_candidate()))
        score = gen.get_fitness(gen.get_best_candidate(), variables)
            #abs( evaluate(gen.get_best_candidate(), variables) - TARGET_VAL)


        print("Score: "+str(score/sum(i*i for i in input_array)))
        if score/sum(i*i for i in input_array) < 0.01: # if you reach 1% error, break
            break
        print()
            #gen.evolve(1,0.4,0)
        gen.evolve(1, 0.8, 0.1)
        genNum = genNum + 1
        if (genNum > MAX_GEN_NUM):
            best_of_runs.append(best_candidate)
            genNum = 0
            break
#except: TypeError:
#    pass
#except KeyboardInterrupt:
    #pass

best_of_runs.append(best_candidate)

print("Randomly Generated Function: " + to_lisp(best_candidate))
print(f"Evaluate Results: {evaluate(best_candidate, variables)}")

output_array = []
lowest_score = float_info.max
best_cand_of_runs = best_of_runs[0]
for l in best_of_runs:
    curr_score = gen.get_fitness(l, variables)
    if curr_score < lowest_score:
        lowest_score = curr_score
        best_cand_of_runs = l


for i in range(len(input_array)):
    variables['x'] = i
    #output_array.append(evaluate(best_cand_of_runs, variables))
    output_array.append(evaluate(best_candidate, variables))

#print(best_of_runs)

print("Best Total Candidate: "+to_lisp(best_cand_of_runs))

plt.plot(input_array)
plt.plot(output_array)
plt.show()
