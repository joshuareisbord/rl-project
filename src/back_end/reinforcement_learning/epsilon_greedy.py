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
    directions = ['North', 'South', 'East', 'West']
    moves = qtable.get_state_values(state) # gets the Q-values (moves) for the current state
    random_prob = random.random() # random number between 0 and 1
    action_num = len(actions)
    new_moves = [0] * action_num
    if 'North' in actions:
        idx = actions.index('North')
        new_moves[idx] = moves[0]
    if 'East' in actions:
        idx = actions.index('East')
        new_moves[idx] = moves[1]
    if 'South' in actions:
        idx = actions.index('South')
        new_moves[idx] = moves[2]
    if 'West' in actions:
        idx = actions.index('West')
        new_moves[idx] = moves[3]
    # random move taken with probability epsilon
    if random_prob < epsilon:
        choices = list(zip(moves, actions))
        if choices == []:
            return random.choice(directions)
        return random.choice(choices)[1] # get random move [north, east, south, west]
        
    # greedy move
    return rand_argmax(new_moves, actions)# get greedy move [north, east, south, west]