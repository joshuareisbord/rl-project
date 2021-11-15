
class Simulator:

    def __init__(self, environment):
        self.environment = environment
    
    def get_next_state(self):
        pass
        
    def get_reward(self):
        pass
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
        


        
        




"""
if __name__ == '__main__':
    length = 5
    width = 4
    board = [
            1, 1, 1, 1,
            1, 0, 0, 1,
            1, 0, 1, 1,
            1, 0, 0, 1,
            1, 1, 1, 1
            ]
    
    actions = [-4, 1, 4, -1] # [ north, east, south, west] (index modifiers for the board)
    bounds = [0, [4, 8, 12, 16, 20], 20, [-1, 3, 7, 11, 15]] # [ north, [east], south, [west] ]

    e = Environment(length, width, board, bounds, actions)

    path = e.a_star(0, 19)
    print(path)
    direction = e.get_direction_of_a_star(path)
    print(direction)
    s = States()
    print(s)
"""