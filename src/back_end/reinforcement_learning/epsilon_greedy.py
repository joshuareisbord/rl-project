from back_end.reinforcement_learning.qtable import QTable, State
from back_end.reinforcement_learning.rand_argmax import rand_argmax
import random

def epsilonGreedy(qtable: QTable, state: State, actions, epsilon=0.1):
    """
    Purpose:
        Gets an action given a state based on a epsilon greedy policy.
    Args:
        qtable - the Qtable.
        state - the current state.
        actions - list of actions that can be taken in the current state.
        epsilon - the epsilon value.
    Returns:
        A greedy or random action.
    """
    if 'Stop' in actions:
        actions.remove("Stop")
    # Gets the Q-values (moves) for the current state,
    moves = qtable.get_state_values(state)
    # Get random number between 0 and 1
    random_prob = random.random()
    # The following code is used to keep the index relation of 
    # actions that can be taken, and the action values in move. 
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
            return random.choice(['North', 'East', 'South', 'West'])
        return random.choice(choices)[1] # get random move [north, east, south, west]
    # greedy move
    return rand_argmax(new_moves, actions)# get greedy move [north, east, south, west]