import numpy as np
import random

def rand_argmax(moves, actions):
    """
    Purpose:
        Gets the action that has the highest state-action value.
    Args:
        moves - state-action values stored in the QTable.
        actions - the actions for each move value. 
    Returns: 
        The action that has the highest state-action value. If two or more 
        move values are equal, one of the actions is chosen arbitrarily.
        If in a terminal state, a random action is returned.
    """    
    max_val = float('-inf')
    max_elems = []
    # Loops through each valid action and the respective value from the qtable.
    for val, action in zip(moves, actions):
        # Check if the state-action pair value is better than the max value.
        if val > max_val:
            # Update new max value its action.
            max_val = val
            max_elems = [action]
        # Check if the state-action pair value is equal to the max.
        elif val == max_val:
            # Add action to list of actions that maximize value.
            max_elems.append(action)
    # Only one best action.
    if len(max_elems) == 1:
        return max_elems[0]
    # Terminal state, returns a random action.
    if max_elems == []:
        return  random.choice(['North', 'East', 'South', 'West'])
    # Randomly choose one of the best actions found.
    return random.choice(max_elems)
