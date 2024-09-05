# Genetic Programming for Predicting COVID-19 Infection Rates

## Overview
This project implements a genetic programming algorithm to predict COVID-19 infection rates. The algorithm evolves mathematical functions to fit a dataset of weekly infection rates, demonstrating the application of evolutionary computation techniques to real-world data analysis.

## Key Features
- Function representation using recursive tree structures
- Implementation of genetic operators: mutation (cut and grow, shrink, hoist, reparameterization) and crossover
- Cost function incorporating both prediction accuracy and function complexity
- Generation-based evolution with adjustable genetic operation probabilities
- Testing against real COVID-19 infection rate data

## Implementation Details
- Language: Python 3.10.0
- Key modules:
  - `function_tree.py`: Implements function trees and random generation
  - `genetic_operators.py`: Implements selection, mutation, and crossover operations
  - `generation_functions.py`: Implements the Generation class and evolution methods
  - `datatesting.py`: Handles testing against the real dataset

## Results
- The algorithm successfully generated functions to model COVID-19 infection rates
- Best performing candidate achieved a score of 0.3529 (lower is better)
- Observed evolutionary strategies: edge-peak-focus and mean-curve-matching

## Future Work
- Improve convergence consistency
- Explore alternative genetic operator selection strategies
- Incorporate more parameters (age, gender, occupation) for more detailed analysis

## Contributors
- Jovanovic, Marko
- Kuppers, Lukas
- Bennett, Matthew

## Acknowledgements
This project was completed as part of CMPT 417/827 X100 under the guidance of Professor Hang Ma.

## Guide to running the program

The Genetic Programming algorithm can easily be run via the below command. Depending on the user system, `python` may need to be replaced by `py` or `python3`.

```
python ./src/main.py
```
