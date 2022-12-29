from typing import Dict
from random import random, randint, choice, randrange, gauss

from function_tree import (
    FunctionTree, get_random_func, get_random_constant, CHILDREN_KEY, NAME_KEY, MAX_DEPTH, 
    CONSTANT_NAME, VALUE_KEY)


def cut_and_grow(root: FunctionTree, values: Dict[str, float], max_depth: int = MAX_DEPTH) -> FunctionTree:
    """Apply cut and grow mutation to tree with root 'root'.
    'values' is a dictionary of all possible values in the problem domain (variables and constants).
    'max_dept' is the max depth of the entire tree. Returns the mutated tree.
    """
    cut_prob = 1.0 / max_depth
    if not root[CHILDREN_KEY] or len(root[CHILDREN_KEY]) == 0 or random() < cut_prob: 
        # cut at current node
        return get_random_func(values,round(abs(gauss(max_depth-1,2))+1))
    # cut in a child node
    rand_child_index = randint(0, len(root[CHILDREN_KEY]) - 1)
    root[CHILDREN_KEY][rand_child_index] = cut_and_grow(root[CHILDREN_KEY][rand_child_index], values, max_depth - 1)
    return root


def shrink(root: FunctionTree) -> FunctionTree:
    """Apply shrink mutation to tree with root 'root'.
    Returns the mutated tree.
    """
    if not root[CHILDREN_KEY] or len(root[CHILDREN_KEY]) == 0:
        return root
    large_subtrees = []
    for i in range(len(root[CHILDREN_KEY])):
        child = root[CHILDREN_KEY][i]
        if child[CHILDREN_KEY] and len(child[CHILDREN_KEY]) > 0:
            large_subtrees.append(i)
    if len(large_subtrees) == 0 or random() > 0.666:
        # perform shrink on current node
        return _get_random_leaf(root)
    # perform shrink on subtree
    rand_index = choice(large_subtrees)
    root[CHILDREN_KEY][rand_index] = shrink(root[CHILDREN_KEY][rand_index])
    return root


def hoist(root: FunctionTree) -> FunctionTree:
    """Apply hoist mutation to tree with root 'root'.
    Returns the mutated tree.
    """
    if not root[CHILDREN_KEY] or len(root[CHILDREN_KEY]) == 0 or random() > 0.5:
        return root
    rand_subtree = choice(root[CHILDREN_KEY])
    return hoist(rand_subtree)


def _get_random_leaf(root: FunctionTree) -> FunctionTree:
    """Gets random leaf in tree rooted at 'root'."""
    if not root[CHILDREN_KEY] or len(root[CHILDREN_KEY]) == 0:
        return root
    rand_child = choice(root[CHILDREN_KEY])
    return _get_random_leaf(rand_child)


def reparameterization(root: FunctionTree) -> FunctionTree:
    """Gives each constant a 50/50 chance of taking on a new random value."""
    if root[NAME_KEY] == CONSTANT_NAME: # node is a constant
        if random() < 0.5:
            root[VALUE_KEY] = get_random_constant()
        return root
    if root[CHILDREN_KEY] is not None and len(root[CHILDREN_KEY]) > 0:
        for i in range(len(root[CHILDREN_KEY])):
            root[CHILDREN_KEY][i] = reparameterization(root[CHILDREN_KEY][i])
    return root


def crossover(rootA: FunctionTree, rootB: FunctionTree, max_depth: int = MAX_DEPTH):
    """Takes two function trees and performs a crossover, randomly swapping subtrees (Subtree can be the entire tree).
    Returns list of the two crossed-over trees.
    """
    cut_prob = 1.0/max_depth

    curr_Node_A = rootA
    parent_curr_node_A = None
    while(curr_Node_A[CHILDREN_KEY] is not None and len(curr_Node_A[CHILDREN_KEY]) != 0 and random() > cut_prob):
        parent_curr_node_A = curr_Node_A
        curr_Node_A = curr_Node_A[CHILDREN_KEY][randrange(0,len(curr_Node_A[CHILDREN_KEY]))]
    cut_from_tree_A = curr_Node_A.copy()


    parent_curr_node_B = None
    curr_Node_B = rootB
    while(curr_Node_B[CHILDREN_KEY] is not None and len(curr_Node_B[CHILDREN_KEY]) != 0 and random() > cut_prob):
        parent_curr_node_B = curr_Node_B
        curr_Node_B = curr_Node_B[CHILDREN_KEY][randrange(0,len(curr_Node_B[CHILDREN_KEY]))]        
    cut_from_tree_B = curr_Node_B.copy()

    if (parent_curr_node_A is not None):
        parent_curr_node_A[CHILDREN_KEY].remove(cut_from_tree_A)
        parent_curr_node_A[CHILDREN_KEY].append(cut_from_tree_B)
    else:
        rootA = cut_from_tree_B


    if (parent_curr_node_B is not None):
        parent_curr_node_B[CHILDREN_KEY].remove(cut_from_tree_B)
        parent_curr_node_B[CHILDREN_KEY].append(cut_from_tree_A)
    else:
        rootB = cut_from_tree_A
    
    return [rootA, rootB]


def random_mutation(root: FunctionTree, values: Dict[str, float]) -> FunctionTree:
    repamselect = randint(0, 100)
    selection = randint(0,2)

    if repamselect < 5:
        return reparameterization(root)

    if (selection == 0):
        return cut_and_grow(root, values)

    if (selection == 1):
        return shrink(root)

    if (selection == 2):
        return hoist(root)

#    if (selection == 3):
#        return reparameterization(root)
