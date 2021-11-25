import numpy as np
import random

def rand_argmax(arr):
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
    max_val = float('-inf')
    max_elems = []

    for elem in enumerate(arr):
        curr = elem[1]
        idx = elem[0]
        if curr > max_val: # if elem is bigger then max value, then replace max value and list
            max_val = curr
            max_elems = [elem]
        elif curr == max_val: # if equal to max, append to list of max elements
            max_elems.append(elem)

    if len(max_elems) == 1: # only one element then it is the max
        return max_elems[0]
    
    return random.choice(max_elems) # (index, value)

if __name__ == "__main__":
    directions = ['north', 'south', 'east', 'west']
    lst = [0, 0, 1, 1]
    print(directions[rand_argmax(lst)[0]])