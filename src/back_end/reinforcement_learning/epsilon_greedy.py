from qtable import QTable, State
import random

def epsilonGreedy(qtable: QTable, state: State, actions, epsilon=0.1):
    """
    epsilon-greedy policy

    :param qtable: Q-table
    :param state: the current state as a State object
    :param epsilon: epsilon
    :return: action
    """

    moves = qtable.getValues(state) # gets the Q-values (moves) for the current state
    random_prob = random.random() # random number between 0 and 1

    # random move taken with probability epsilon
    if random_prob < epsilon:
        choices = list(zip(moves, actions))
        return random.choice(choices)[1] # get random move [up, down, left, right]
        
    # greedy move
    return max(zip(moves, actions), key=lambda x:x[0])[1] # get greedy move [up, down, left, right]