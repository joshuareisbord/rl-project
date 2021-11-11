
class Action:
    
    def __init__(self, action):
        self.action = action
        self.reward = 0
        self.n = 5
        self.m = 4

    def get_next_state(self, state):
        is_valid = self.valid_action(state)
        if not is_valid:
            self.reward = 0
            return state
        if self.action == 'N':
            return self.update_state(state, -self.m)
        if self.action == 'S':
            return self.update_state(state, self.m)
        if self.action == 'E':
            return self.update_state(state, 1)
        if self.action == 'W':
            return self.update_state(state, -1)

    def update_state(self, state, value):
        pill_eaten = self.collected_pill(state)
        self.get_reward(pill_eaten)
        current_pac_man_pos = state[0]
        new_pac_man_pos = current_pac_man_pos + value
        state[0] = new_pac_man_pos
        if pill_eaten:

            state[2][new_pac_man_pos] = 2
        return state

    def valid_action(self, state):

        # Checks if player is going to move into N, S border
        if self.action == 'N':
            if (state[0] - 4) < 0:
                return False
            return True
        if self.action == 'S':
            if (state[0] + 4) > (self.n * self.m - 1):
                return False
            return True

        # Checks if player is going to move into E, W border
        if self.action == 'E':
            # check if player is going to move to off the E border
            if (state[0] % self.m -1 == 0):
                return False
            # check if player is going to move to a wall
            if (state[0] + 1 == 0):
                return False
            return True
            
        if self.action == 'W':
            # check if player is going to move to off the W border
            if (state[0] % self.m == 0):
                return False
            # check if player is going to move to a wall
            if (state[0] - 1 == 0):
                return False
            return True
            
        return True

    def get_reward(self, pill_eaten):
        """
        """
        if pill_eaten: 
            self.reward = 1
            return
        self.reward = 0
        return
        
    def collected_pill(self, state):
        """
        """
        pac_man = state[0]
        if self.action == 'N':
            if state[2][pac_man - 4] == 2:
                return False
            return True
        if self.action == 'E':
            if state[2][pac_man + 1] == 2:
                return False
            return True
        if self.action == 'S':
            if state[2][pac_man + 4] == 2:
                return False
            return True
        if self.action == 'W':
            if state[2][pac_man - 1] == 2:
                return False
            return True


    