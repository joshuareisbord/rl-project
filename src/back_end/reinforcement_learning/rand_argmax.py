import numpy as np

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
    max_val = np.max(arr)
    maxed_elems = []
    for i in range(len(arr)):
        if (arr[i] == max_val):
            maxed_elems.append(i)
    rand = np.random.randint(len(maxed_elems))
    return maxed_elems[rand]