import numpy as np
import random

def rand_argmax(moves, actions):
    """
    Purpose:
        Function finds the index of the element with the highest value
        if mulitple values are the highest, it randomly selects one of
        the elements.
    Args:
        arr - array object, where elements are comparable
    Returns: 
        returns the index of the highest 
    """
    
    # find the index of the highest value
    directions = ['North', 'South', 'East', 'West']
    max_val = float('-inf')
    max_elems = []
    for val, action in zip(moves, actions):
        
        if val > max_val: # if elem is bigger then max value, then replace max value and list
            max_val = val
            max_elems = [action]
        elif val == max_val: # if equal to max, append to list of max elements
            max_elems.append(action)

    if len(max_elems) == 1: # only one element then it is the max
        return max_elems[0]
    
    if max_elems == []:
        return  random.choice(directions)
    return random.choice(max_elems)
