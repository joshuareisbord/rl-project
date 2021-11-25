from back_end.reinforcement_learning.qtable import QTable, State
import random
from back_end.reinforcement_learning.rand_argmax import rand_argmax

def epsilonGreedy(qtable: QTable, state: State, actions, epsilon=0.1):
    """
    epsilon-greedy policy

    :param qtable: Q-table
    :param state: the current state as a State object
    :param epsilon: epsilon
    :return: action
    """
    try:
        actions.remove("Stop")
    except ValueError:
        pass

    moves = qtable.get_state_values(state) # gets the Q-values (moves) for the current state
    random_prob = random.random() # random number between 0 and 1
    new_moves = []
    if 'North' in actions:
        new_moves.append(moves[0])
    if 'East' in actions:
        new_moves.append(moves[1])
    if 'South' in actions:
        new_moves.append(moves[2])
    if 'West' in actions:
        new_moves.append(moves[3])
    # random move taken with probability epsilon
    if random_prob < epsilon:
        choices = list(zip(moves, actions))
        if choices == []:
            return "North"
        return random.choice(choices)[1] # get random move [north, east, south, west]
        
    # greedy move
    return rand_argmax(moves, actions)# get greedy move [north, east, south, west]