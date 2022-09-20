from typing import Dict
from random import random, choice, uniform
from numpy.random import normal
from operators import OPERATORS, EVAL_KEY, NUM_ARGS_KEY
from sys import float_info
"""
Function tree is made up of nodes which are simply a dictionary of the form:
{
    name: <value name or operator name - set to CONSTANT if node is a constant leaf>, 
    children: <list of children nodes>, 
    value: <constant value or null, if node is a variable or operator>
}
"""

CONSTANT_NAME = "CONSTANT"
NAME_KEY = "name"
CHILDREN_KEY = "children"
VALUE_KEY = "value"
MAX_DEPTH = 4
MIN_RAND_CONSTANT = -100
MAX_RAND_CONSTANT = 100
FunctionTree = Dict[str, object]


def evaluate(subtree: FunctionTree, values: Dict[str, float]) -> float: 
    try:
        if not subtree:
            print(f"function_tree:Warning: subtree root {subtree[NAME_KEY]} is null")
            return 0
        if subtree[NAME_KEY] not in OPERATORS:   # node is a leaf (value)
            if subtree[NAME_KEY] == CONSTANT_NAME:  # node is a constant
                return subtree[VALUE_KEY]
            if subtree[NAME_KEY] not in values:
                print(f"FunctionTree:Warning:Value {subtree[NAME_KEY]} not specified")
                return 0
            return values[subtree[NAME_KEY]]
        # node is an operator. Get child values and evaluate
        arguments = [evaluate(x, values) for x in subtree[CHILDREN_KEY]]
        return OPERATORS[subtree[NAME_KEY]][EVAL_KEY](*arguments)
    except:
        return float_info.max


def to_lisp(subtree: FunctionTree) -> str:
    try:
        if not subtree:
            return ""
        if subtree[NAME_KEY] not in OPERATORS:
            if subtree[NAME_KEY] == CONSTANT_NAME:
                return ("%.2f"%(subtree[VALUE_KEY]))
            return subtree[NAME_KEY]
        child_expressions = [to_lisp(x) for x in subtree[CHILDREN_KEY]]
        children_str = " ".join(child_expressions)
        return f"({subtree[NAME_KEY]} {children_str})"
    except RecursionError:
        return ""

def get_random_func(values: Dict[str, float], max_depth: int = MAX_DEPTH, startFlag: bool = True) -> Dict:
    leaf_prob = 1.0 / max_depth
    if random() < leaf_prob or max_depth <= 1:  # generate a constant / variable
        if random() < 0.5 or startFlag: # generate a variable leaf
            rand_var = choice(list(values.keys()))
            return { NAME_KEY: rand_var, CHILDREN_KEY: None, VALUE_KEY: None }
        rand_val = get_random_constant()
        return { NAME_KEY: CONSTANT_NAME, CHILDREN_KEY: None, VALUE_KEY: rand_val }
    # generate operator and its children
    rand_op = choice(list(OPERATORS.keys()))
    children = []
    for _ in range(OPERATORS[rand_op][NUM_ARGS_KEY]):
        children.append(get_random_func(values, max_depth - 1, False))
    return {
        NAME_KEY: rand_op, 
        CHILDREN_KEY: children, 
        VALUE_KEY: None
    }


def get_random_constant() -> float:
    return normal(0, 100)
