import numpy as np

from state import State

class Environment:
    """
    
    """

    def __init__(self):
        """
        
        """
        self.board = [
            1, 1, 1, 1,
            1, 0, 0, 1,
            1, 0, 1, 1,
            1, 0, 0, 1,
            1, 1, 1, 1
        ]
        self.state = [0, 19, self.board]
        # self.n = self.board.shape[0]
        # self.m = self.board.shape[1]
        self.states = []
        # self.generate_states()
        self.bfunction(self.state.copy())
        print(self.states)
        self.actions = None
        self.rewards = None
    
    def set_state(self):
        pass
    
    def get_state(self):
        pass

    def generate_states(self):
        """
        
        """
        # states = []
        walls = []
        non_walls = []
        for elem in self.board:
            if elem == 0:
                walls.append(elem)
            else:
                non_walls.append(elem)

        for i in range(2**len(non_walls)):
            pellet_s = list(bin(i)[2:].zfill(len(non_walls)))
               
            for wall in walls:
                pellet_s.insert(wall, 0)
                for p in range(len(self.board)):
                    for g in range(len(self.board)):
                        if not (p in walls or g in walls):
                            print([p,g,pellet_s])
                            self.states.append([p,g,pellet_s])

    def bfunction(self, current_state, states, visited_states):
        if not states:
            return 
        # print(state)
        # if state in self.states:
        #     return
        # if state not in self.states:
        #     self.states.append(state)
        # state_obj = State(state)
        # self.bfunction(state_obj.action_set[0].get_next_state(state))
        # self.bfunction(state_obj.action_set[1].get_next_state(state))
        # self.bfunction(state_obj.action_set[2].get_next_state(state))
        # self.bfunction(state_obj.action_set[3].get_next_state(state))
        # return

    def validate_state(self, state):
        """
        Function will return true if state can be visited, false otherwise.
        """
        pass

    def set_action(self, action, index):
        """
        """
        self.actions[index] = action
    
    def get_action(self, index):
        """
        """
        return self.actions[index]

    def generate_actions(self):
        """
        
        """
        self.actions = np.ndarray([])
        

    def generate_rewards(self):
        """
        
        """
        pass

if __name__ == '__main__':
    # print("here")
    e = Environment()


    
