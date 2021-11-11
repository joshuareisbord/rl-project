from action import Action

class State:
    
    def __init__(self, state):
        """
        """
        # Policy will be updated later
        self.policy = None
        self.state = state
        self.action_set = self.generate_actions()
        
    def generate_actions(self):
        """
        Function generates North, East, South, and West action objects.
        """
        return [Action('N'), Action('E'), Action('S'), Action('W')]

    def update_policy(self, action):
        """
        Function updates the policy.
        """
        self.policy = action

    # Might not need now
    # def get_actions_set(self):
    #     return self.action_set

    # def get_policy(self):
    #     return self.policy

    # def get_state(self):
    #     return self.state

    # def set_action_set(self, a_set):
    #     self.action_set = a_set

    # def set_policy(self, p):
    #     self.policy = p

    # def set_state(self,s):
    #     self.state = s
