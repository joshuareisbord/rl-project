from util.interpreter import get_closest_pellet_direction, get_ghost_direction
from util.state import State

class Simulator:

    def __init__(self, environment):
        self.environment = environment

    def move_ghost(self):
        timestep = self.environment.timestep
        a_star = True
        if (timestep / 4) % 2 == 0:
            #Activate a_star Behaviour
            a_star = True
        else:
            a_star = False

        if(a_star):
            ghost_path,_ = self.environment.a_star.a_star(self.environment.ghost, self.environment.pac_man)
        
    def run_simulation(self):
        pass

    def get_next_state(self, pac_man_position, action):
        """
        Returns state hash to look up the states value in the q table.
        """
        node = self.environment.nodes[pac_man_position]
        pac_man_next_position = pac_man_position + self.environment.actions[action]
        next_node = self.environment.nodes[pac_man_next_position]
        state = []
        
        if next_node == None:
            return state, pac_man_position
        
        for index, _ in enumerate(self.actions):
            valid = self.environment.verify_position(pac_man_next_position, index)
            if valid:
                state.append(1)
            else:
                state.append(0)

        state.append(get_closest_pellet_direction(self.environment))
        # Change here if more ghosts are added.
        state.append(get_ghost_direction(self.environment))
        state = State(state[0], state[1], state[2], state[3], state[4], state[5])
        state_hash = state.__hash__()
        return state_hash, pac_man_next_position
        
        


