import numpy as np

from state import State, States
from qtable import QTable
from back_end.util import rand_argmax

class SARSA:
    """

    """

    def __init__(self, environment, epsilon=0.05, gamma=0.9):
        """

        """
        self.env = environment
        self.epsilon = epsilon
        self.gamma = gamma
        self.state = States()
        self.qtable = QTable()
        self.init_state = State(0, 1, 1, 0, 1, 1)
        self.init_state_hash = self.init_state.__hash__()
        self.pac_man_position = 0


    def sample(self):
        action = self.epsilon_greedy()
        reward = self.env.get_reward(self.pac_man_position, action)
        next_state, self.pac_man_position = self.env.get_next_state(self.pac_man_position, action)

            
    def epsilon_greedy(self, state):
        not_greedy = np.random.rand()
        if not_greedy < self.epsilon:
            # Get random action
            action = np.random.randint(4)  
        else:
            # Get greedy action
            state_action_pairs = self.qtable.get_state_q_values(state)
            action = rand_argmax(state_action_pairs)
                
        return action

    